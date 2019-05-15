var AOIController = function($scope, $http, $location) {
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

    /***** Server communications block *****/
    $scopeGlobal.ws = new WebSocket("ws://localhost:8888/websocket");
    $scopeGlobal.ws.onmessage = function (evt) {
        alert(evt.data)
    };
    /***************************************/
    // Fetch the conditions
        $http.get('static/data_updated/conditions.json').
        success(function(data, status, headers) {
            $scope.conditions = data;
            for (let condition in $scope.conditions) {
                $http.get('static/data_updated/' + $scope.conditions[condition] + '_updated.json').
                success(function(data, status, headers) {
                    // Reset the worker filter
                    $scope.imgSrc = 'static/' + data.chart;
                    $scope.curText = data.text;
                    $scope.datatable = data.datatable;
                    $scope.marks = data.marks;
                    $scope.visualReferences = data.visual_references;
                    $scope.curReference = data.references;
                    let startEndCoords = [];
                    Object.keys($scope.curReference).forEach(function(key) {
                        startEndCoords.push({"refId": key, "start": $scope.curReference[key]['sentence_start_char'], "end": $scope.curReference[key]['sentence_end_char']})
                    });
                    document.getElementById("theText").innerHTML =$scope.curText;
                    $scope.coordinatesofChar = findCoordinatesofCharacters("#theTextParagraph");
                    $scope.coordinatesofRefSentences = findCoordinatesofRefSentences("#theTextParagraph", $scope.coordinatesofChar, startEndCoords);
                    writePolygonToDb($scope.coordinatesofRefSentences, $scope.conditions[condition]);
                });
            }
            // $scopeGlobal.ws.send("done_generating");in
        });

    angular.element(document.getElementById('theChart')).on('load',
        function() {
            initReferences($scope);
        });
};
