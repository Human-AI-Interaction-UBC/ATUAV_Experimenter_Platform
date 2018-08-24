var AppCtrl = function($scope, $http, $location) {
  /**
   * The URL to query for condition information. Initialized in
   * highlight_root.html
   * @type {string}
   */
  $scope.loadUrl;
  $scopeGlobal = $scope;

  /**
   * Source for the chart.
   * @type {string}
   */
  $scope.imgSrc = '';

  /** @type {number} */
  $scope.condition;
  /** @type {Array.<number>} */
  $scope.conditions;

  /** @type {number} */
  $scope.curConditionId;

  /**
   @type {{
     passed: {Array.<Reference>},
     failed: {Array.<Reference>},
     gold: {Array.<Reference>},
     combined: {Array.<Reference>}
   }}
   */
  $scope.allReferences;

  /** @type {Reference} */
  $scope.curReference;

  /** @type {Object.<string, (number|string)>} */
  $scope.filters = {
    workerIndex: 0,
    expandToSentence: false,
    /**
     * If true, require user to select all of the text in a reference before it is
     * highlighted.
     * @type {string} One of "strict", "lenient", "hybrid", or "sentence"
     */
    matchMode: 'lenient'
  };
  /***** Server communications block *****/
  $scopeGlobal.interventions = {};
  $scopeGlobal.ws = new WebSocket("ws://localhost:8888/websocket");
  // Generic app.js functions for triggering/dremoving interventions
  $scopeGlobal.ws.onmessage = function (evt) {
    var obj = JSON.parse(evt.data);
    //console.log(evt.data);
    if (obj.remove != null) {
        handleRemoval(obj);

    } else if (obj.deliver != null) {
        handleDelivery(obj);
    }
  }
  /***************************************/

  $scope.curMarksManager;
  $scope.curSpanManager;
  console.log(currentMMD);
  // Fetch the conditions
  $http.get('static/data/conditions.json').
      success(function(data, status, headers) {
        $scope.conditions = data;
        if (data.length > 0) {
          $scope.curConditionId = data[0];
            if(currentMMD){
                $scope.curConditionId = currentMMD;
            }
          $scope.changeConditions();
        }
      });

  $scope.changeConditions = function() {
    console.log('change conditions');

    if ($scope.curSpanManager) {
      $scope.curSpanManager.clearSpans();
    }
    //console.log('static/data/' + $scope.curConditionId + '.json');
    // Load the new condition
    $http.get('static/data/' + $scope.curConditionId + '.json').
        success(function(data, status, headers) {
          // Reset the worker filter
          $scope.imgSrc = 'static/' + data.chart;
          $scope.curText = data.text;
          globalText = data.text;
          $scope.sentences = data.sentences;
          //console.log($scope.curText);
          //console.log($scope.sentences);
          $scope.datatable = data.datatable;
          $scope.marks = data.marks;
          $scope.visualReferences = data.visual_references;
          $scope.allReferences = data.references;
          $scope.curReference = $scope.allReferences[1].reference; // '1== GOLD reference
          //$scope.curReference = $scope.allReferences
          $scope.selectedReference = 0
          $scope.lastSelectedReference = -1
          //console.log(JSON.stringify($scope.curReference));

          document.getElementById("theText").innerHTML =$scope.curText;

          $scope.coordinatesofChar = findCoordinatesofCharacters("#theTextParagraph");
          $scope.coordinatesofSentences = findCoordinatesofSentences("#theTextParagraph", $scope.coordinatesofChar);
          $scope.coordinatesofWords = findCoordinatesofWords("#theTextParagraph", $scope.coordinatesofChar);
          console.log("CHARACTERS")
          console.log($scope.coordinatesofChar)
          console.log("SENTENCES")
          console.log($scope.coordinatesofSentences)
          console.log("WORDS")
          console.log($scope.coordinatesofWords)

          $scope.aggregatedData = aggregateDataIntoJSON($scope.coordinatesofChar, $scope.coordinatesofSentences, $scope.coordinatesofWords);
          console.log("AGGREGATE")

          console.log($scope.aggregatedData);

          //uncomment this to store the json data
          //sendJSONtoTornado($scope.aggregatedData,$scope.curConditionId );

          //console.log($scope.coordinatesofSentences[1].polygonCoords);
          //drawOverlay($scope.coordinatesofSentences[1].polygonCoords);

          //select ref from drop-down
          var selectHtml = "";

            for(var j=0;j<$scope.curReference.length;j++){
              selectHtml+= '<option value="'+j+'">'+j+'</option>';
            }

          $("#referenceSelect").html(selectHtml);

          $("#referenceSelect").change(function() {
              //alert($(this).find("option:selected").text()+' clicked!');
              var currentReference = $(this).find("option:selected").text();
              onReferenceChange(parseInt(currentReference));
              //loadMMD(currentMMD);
      });

      //Highlighting bassed on marked references
      console.log($scope.datatable);
      $http.get('static/data/' + "combined_references" + '.json').
      success(function(data, status, headers) {
        console.log(data);
        for(var i=0;i<data.length;i++){
          console.log(data[i].mmd_id,$scope.curConditionId);
          if (data[i].mmd_id===$scope.curConditionId){
            $scope.merged_refs = data[i].merged_refs;
          }
        }
      });
    });
  };

  $scope.updateCondition = function() {
    initReferences($scope);
  };

  $scope.onReferenceSelect = function(ref) {
    ref.selected = !ref.selected;
    var overlappedReferences = [];
    for (var i=0; i<$scope.curReference.length; i++) {
      var reference = $scope.curReference[i];
      if (reference.selected) {
        overlappedReferences.push(reference);
      }
    }
    highlightRelatedTuples($scope, overlappedReferences, reference.selected); //TODO: might be bad code: pls fix
    highlightRelatedPhrases($scope, overlappedReferences, reference.selected);
  }

  angular.element(document.getElementById('theChart')).on('load',
      function() {
        initReferences($scope);
      });
};
