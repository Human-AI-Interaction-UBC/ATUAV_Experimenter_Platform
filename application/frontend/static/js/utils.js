(function(){

var utils = {
  loadJSON: function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.setRequestHeader("Content-Type", "text/json");
    xhr.onreadystatechange = function() {
      // If the request is complete and successful
      if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        callback.call(null, xhr.responseText);
      }
    };
    xhr.send();
  },

  loadData: function(urls, complete) {
    outputs = urls.map(function(val) { return false; });

    for(var i=0; i<urls.length; i++) {
      // Use a closure to assign the correct index to each output.
      loadJSON(urls[i], (function(this_ind) {
        return function(response) {
          outputs[this_ind] = JSON.parse(response);
          
          // Fire the callback when all the data has been fetched.
          var finished = outputs.reduce(function(acc, val) { return acc && isNaN(val); }, true);
          if(finished) {
            complete.apply(null, outputs);
          }
        }
      })(i));
    }
  },

  getReferenceString: function(reference) {
    var phrase_str = reference.phrases.map(function(phrase){
      return '"'+reference.text.substring(phrase.start, phrase.end)+'"';
    }).join(', ');
    var tuple_str = reference.tuples.map(function(tuple){
      return '('+tuple.join(', ')+')';
    }).join(' ');
    return phrase_str + ' | ' + tuple_str;
  },

  createTable: function(data) {
    var headers = data.headers,
      tuples = data.data,
      theTable = document.createElement('table'),
      table = d3.select(theTable)
              .attr('class', 'table table-striped')
              .style('width', 'auto');
    
    // Create the header
    var header = table.append("tr").classed("table-header", true)
                .selectAll("td.table-header").data(headers)
                .enter().append("th").classed("table-header", true)
                .text(function(d) {
                  // Ignore header titles I've made up (prefixed with a '_' in the data)
                  return d.indexOf('_') === 0 ? "" : d;
                });
    
    // Create the tuple rows
    var selectedRE = new RegExp('\\bselected\\b\\s*','g');
    var tupleRows = table.selectAll("tr.tuple")
      .data(tuples, function(d,i) {
        d.index = i;
        return d;
      })
      .enter().append("tr").classed("tuple", true)
      .on('click', function(d,i) {
        // Use classList if available (HTML5)
        if(this.classList) {
          this.classList.toggle('selected');
          return;
        }

        // If classList is not available, do it via regexps
        if(this.className.search(selectedRE) != -1) {
          this.className = this.className.replace(selectedRE, "");
        } else {
          this.className += " selected";
        }
      });
    
    // Create the cells in the tuple
    var cells = tupleRows.selectAll("td.tuple").data(function(d) { return d.tuple ? d.tuple : d; })
              .enter().append("td").classed("tuple", true)
              .text(function(d){
                return d;
              });

    return theTable;
  },

  equalTuples: function(ta, tb) {
    if(ta.tuple) ta = ta.tuple;
    if(tb.tuple) tb = tb.tuple;

    if(ta.length != tb.length) return false;

    for(var i=0; i<ta.length; i++) {
      if(ta[i] !== tb[i]) return false;
    }

    return true;
  },

  visualReferenceClickHandler: function(selectionManager, marksManager, visrefs, datatable, data) {
    var ref_tuples;
    if(d3.event.target.tagName === 'PRE') {
      // Highlight the selected text
      if(data.phrases.length > 0) {
        selectionManager.setSelections(data.phrases);
      }

      ref_tuples = data.tuples;
      if(ref_tuples[0].id) {
        ref_tuples = ref_tuples.map(function(val) {
          return val.tuple;
        });
      }

      // Highlight the marks

      // Get the tuple ids
      var tuple_ids = [];
      data.tuples.forEach(function(tuple) {
        datatable.data.forEach(function(d) {
          if(utils.equalTuples(d.tuple,tuple)) {
            tuple_ids.push(d.id);
          }
        });
      });

      // Get the marks from the visrefs table
      var selected_mark_ids = [];
      for(var markId in visrefs) {
        if(visrefs.hasOwnProperty(markId)) {
          visrefs[markId].tuple_ids.forEach(function(tuple_id) {
            tuple_ids.forEach(function(selected_id) {
              if(selected_id === tuple_id) selected_mark_ids.push(markId);
            });
          });
        }
      }

      // Highlight the marks
      marksManager.marks.classed('selected', function(d) {
        for(var i=0; i<selected_mark_ids.length; i++) {
          if(selected_mark_ids[i] == d.id) return true;
        }
        return false;
      });
    }
  },

  referenceClickHandler: function(selectionManager, table, data) {
    var ref_tuples;
    if(d3.event.target.tagName === 'PRE') { // Don't highlight if the user clicks the cncel button
      // Highlight the selected text
      if(data.phrases.length > 0) {
        selectionManager.setSelections(data.phrases);
      }

      ref_tuples = data.tuples;
      if(ref_tuples[0].id) {
        ref_tuples = ref_tuples.map(function(val) {
          return val.tuple;
        });
      }

      // Highlight the table rows
      d3.select(table).selectAll('tr.tuple')
        .classed('selected', function(tupleData) {
          var match = false,
            i;
          for(i=0; i<ref_tuples.length; i++) {
            match = true;
            if(tupleData.tuple) tupleData = tupleData.tuple;
            tupleData.forEach(function(elem, ind) {
              if(elem !== ref_tuples[i][ind]) match = false;
            });
            if(match) return true;
          }
          return match;
        });
    };
  }
}

window.utils = utils;

}());
