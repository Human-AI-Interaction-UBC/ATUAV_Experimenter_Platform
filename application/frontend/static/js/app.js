
var ws;
var interventions;
var curMarksManager;
var old_active_interventions;

function init() {
  $.getJSON('static/data_updated/' + 62 + '.json',
      function(data) {
        var marks = data.marks;
        curMarksManager = new MarksManager(marks.marks, document.getElementById('theChart'));
        curMarksManager.createOverlay();
        curMarksManager.changeType(MarksManager.DESATURATE);
      });
}

function highlightVisOnly(referenceID, transition_in, args) {
    //}
  //  removeAllInterventions(referenceID); TODO: commented out
    //setTimeout(function () {
      var tuple_ids = Object.values(interventions).map(function(obj){ return obj.tuple_id});

      //highlightRelatedTuples($scopeGlobal, tuple_ids , referenceID, transition_in, args);
      curMarksManager.highlight(tuple_ids , referenceID.tuple_id, transition_in, args);


    //},transition_in*1.2); //TODO:CHECK
}


function highlightVisOnly_recency(referenceID, transition_in, args) {
    //}
  //  removeAllInterventions(referenceID); TODO: commented out
    //setTimeout(function () {
      var tuple_ids = Object.values(interventions).map(function(obj){ return obj.tuple_id});

      //highlightRelatedTuples($scopeGlobal, tuple_ids , referenceID, transition_in, args);
      curMarksManager.highlight(tuple_ids , referenceID.tuple_id, transition_in, args);

    //},transition_in*1.2); //TODO:CHECK
}

function highlightLegend(referenceID, transition_in, args) {
      curMarksManager.highlightLegend(transition_in, args);
}

function run() {
  ws = new WebSocket("ws://localhost:8888/websocket");
  ws.onmessage = function (evt){
    var obj = JSON.parse(evt.data);
    //console.log(evt.data);
    if (obj.remove != null) {
      console.log("Received a remove call");
      var referenceID;
      for (let intervention of obj.remove) {
        var referenceID = interventions[intervention]
        delete interventions[intervention];
        removeAllInterventions(referenceID);
      }

    } else if (obj.deliver != null) {
      console.log("Received a deliver call");
      console.log(obj.deliver)
      for (let intervention of obj.deliver) {
        var func = intervention.function;
        var interventionName = intervention.name;
        var transition_in = intervention.transition_in;

        var args = JSON.parse(intervention.arguments);
        var referenced_tuples = [];
        var data = $scope.datatable.data;
        if (args.type == "legend") {
          referenced_tuples.push("legend");
        } else {
          var referenceID = args.id;
        }

        interventions[interventionName] = { tuple_id: referenceID, args: args, transition_out: intervention.transition_out };

      //highlightVisOnly($scopeGlobal.selectedReference);

        eval(func)(interventions[interventionName], transition_in, args);
        //console.log('Concat test:', interventions.map(a => a.tuple_id));
        //$scopeGlobal.old_active_interventions = $scopeGlobal.old_active_interventions.concat(interventions.map(a => a.tuple_id));
        //console.log("Timestamp end:");
        //var d = new Date();
        //console.log(d.getTime());
      }

    }
  }
}
