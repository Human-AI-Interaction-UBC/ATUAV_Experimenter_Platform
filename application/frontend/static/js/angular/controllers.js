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
    // Load the new condition
    $http.get('static/data_updated/' + $scope.curConditionId + '_updated.json').
        success(function(data, status, headers) {
          // Reset the worker filter
          $scope.imgSrc = 'static/' + data.chart;
          $scope.curText = data.text;
          globalText = data.text;
          $scope.sentences = data.sentences;
          $scope.datatable = data.datatable;
          $scope.marks = data.marks;
          $scope.visualReferences = data.visual_references;
          $scope.curReference = data.references
          startEndCoords = [];
          for (i = 0; i < Object.keys($scope.curReference).length; i++) {
            startEndCoords.push({"start": $scope.curReference[100 + i]['sentence_start_char'], "end": $scope.curReference[100 + i]['sentence_end_char']})
          }
          $scope.selectedReference = 0;
          $scope.lastSelectedReference = -1;
          document.getElementById("theText").innerHTML =$scope.curText;
          $scope.coordinatesofChar = findCoordinatesofCharacters("#theTextParagraph");
          $scope.coordinatesofSentences = findCoordinatesofSentences("#theTextParagraph", $scope.coordinatesofChar);
          $scope.coordinatesofWords = findCoordinatesofWords("#theTextParagraph", $scope.coordinatesofChar);
          $scope.coordinatesofRefSentences = findCoordinatesofRefSentences("#theTextParagraph", $scope.coordinatesofChar, startEndCoords);
          $scope.aggregatedData = aggregateDataIntoJSON($scope.coordinatesofChar, $scope.coordinatesofRefSentences, $scope.coordinatesofWords);
          console.log($scope.aggregatedData)
          //uncomment this to store the json data
          //sendJSONtoTornado($scope.aggregatedData,$scope.curConditionId );
          console.log($scope.coordinatesofSentences[0].polygonCoords);
          //drawOverlay($scope.aggregatedData.sentenceData[0].polygonCoords);
          //console.log($scope.aggregatedData.sentenceData[0].polygonCoords)
          console.log("drew overlay")

      });
  };
  angular.element(document.getElementById('theChart')).on('load',
      function() {
        initReferences($scope);
      });
};
