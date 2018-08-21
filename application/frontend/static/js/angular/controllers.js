var AppCtrl = function($scope, $http, $location) {
  /**
   * The URL to query for condition information. Initialized in
   * highlight_root.html
   * @type {string}
   */
  $scope.loadUrl;
    $scopeGlobal = $scope;

    /** @type {string} */

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

  $scopeGlobal.interventions = {};

 // TODO: delete
 // begins here:
 // for testing connection between middlend and front-end
  //var handleCallback = function (msg) {
    //  console.log("reached here");
      //console.log(msg.data);
  //};

  //var source = new EventSource('/socket');
  //source.addEventListener('message', handleCallback, false);

  $scopeGlobal.ws = new WebSocket("ws://localhost:8888/websocket");
  $scopeGlobal.ws.onmessage = function (evt){
    var obj = JSON.parse(evt.data);
    //console.log(evt.data);
    if (obj.remove != null) {
        handleRemoval(obj);

    } else if (obj.deliver != null) {
        handleDelivery(obj);
    }
  }

  //ends here

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


        //  The following code was used to adjust the mmd references due to changes made to the original ones
        //MMD: offset
        // 30: 106, 60=0, 62=0, 66=312, 72 =0,
        //74: 146, 76 = 146
        //MERGED ONES
        //4: 687
        //merge:TODO

/*
          var offset =603;
          angular.forEach(data.references, function(reference) {
            console.log(JSON.stringify(reference.reference));
            for (var i=0;i<reference.reference.length;i++){
              for (var j=0;j<reference.reference[i].phrases.length;j++){
                //console.log(JSON.stringify(reference.reference[i].phrases[j].start));
                //console.log(JSON.stringify(reference.reference[i].phrases[j].end));
                reference.reference[i].phrases[j].start+= offset;
                reference.reference[i].phrases[j].end+= offset;

              }

            }

          });
          console.log(JSON.stringify(data.references));
*/


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





          // Add names and select grouping to the references
          angular.forEach($scope.allReferences, function(reference) {
            switch(reference.type) {
              case 'gold':
                reference.name = 'Gold';
                reference.selectType = '';
                break;
              case 'combined':
                reference.name = 'Output';
                reference.selectType = '';
                break;
              default:
                reference.name = 'Worker ' + reference.worker_id;
                if (reference.type === 'passed') {
                  reference.selectType = 'Passed gold';
                } else {
                  reference.selectType = 'Failed gold';
                }
            }
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

  var textPar = angular.element(document.getElementById('theTextParagraph'));
  //document.getElementById("theTextParagraph").innerHTML =globalText;
  textPar.on('mousedown', function() {
    // Clear the spans
    if ($scope.curSpanManager) {
      $scope.curSpanManager.clearSpans();
    }
    // Clear the highlights
    $scope.curMarksManager.unhighlight($scope.curReference); //TODO: Fix up
    angular.forEach($scope.curReference, function(reference) {
      reference.selected = false;
    });
    $scope.$apply();
  });
  textPar.on('mouseup', function() {
    // Get the currently selected words
    var curSelection = window.getSelection();
    if (curSelection.type === 'Range') {
      var start = Math.min(curSelection.anchorOffset, curSelection.focusOffset);
      var end = Math.max(curSelection.anchorOffset, curSelection.focusOffset);
      var selection = {
        start: start,
        end: end
      };
      var references = $scope.curReference;
      var overlappedReferences;

      // Sentence mode
      if ($scope.filters.expandToSentence) {
        var expandedSelection = {
          'start': selection.start,
          'end': selection.end
        };
        angular.forEach($scope.sentences, function(sentence) {
          // Check for sentence overlap with the existing selection
          if ((selection.start >= sentence.start &&
               selection.start <= sentence.end) ||
              (selection.end >= sentence.start &&
               selection.end <= sentence.end)) {
            if (expandedSelection.start > sentence.start) {
              expandedSelection.start = sentence.start;
            }
            if (expandedSelection.end < sentence.end) {
              expandedSelection.end = sentence.end;
            }
          }
        });
        selection = expandedSelection;
      }

      if ($scope.filters.matchMode === 'strict') {
        overlappedReferences = getStrictRelatedReferences(
            selection, references);
      }
      else if ($scope.filters.matchMode === 'lenient') {
        overlappedReferences = getOverlappedReferences(selection, references);
      }
      // Hybrid
      else {
        overlappedReferences = getStrictRelatedReferences(
            selection, references);
        if (overlappedReferences.length === 0) {
          overlappedReferences = getOverlappedReferences(selection, references);
        }
      }

      highlightRelatedTuples($scope, overlappedReferences, selection); //TODO: selection might be bad addition
      highlightRelatedPhrases($scope, overlappedReferences, selection);
      $scope.$apply();
    }
  });
};


var ReferenceDisplayCtrl = function($scope) {
  $scope.mapPhraseIndices = function(phraseObj, text) {
    return text.substring(phraseObj.start, phraseObj.end);
  };

  $scope.mapTuples = function(tuples) {
    return tuples.join(', ');
  };
};
