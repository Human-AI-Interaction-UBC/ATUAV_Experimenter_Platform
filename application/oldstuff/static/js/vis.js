var vis = {};

vis.utils = {};
vis.utils.getTextFromPhraseIndices = function(text, phrases, maxLength) {
  var curString = '';
  var separator = ' | ', seplength = separator.length;
  for (var i=0, len=phrases.length; i < len; i++) {
    nextPhrase = text.substring(phrases[i].start, phrases[i].end);
    if (i < len-1) {
      nextPhrase += separator;
    }
    curString += nextPhrase;
    if (curString.length > maxLength) {
      return curString.substr(0, maxLength);
    }
  }
  return curString;
};

/**
 * Graph has the shape:
 * {
 *   nodes: [{
 *     group: ('gold' | 'candidate')
 *     id: number (independent ids for gold and candidate -- there are (gold,
 *         1) and (candidate, 1) nodes.
 *     reference: Object 
 *   }...]
 *   edges: {
 *     distance: number (0 to 1)
 *     min: boolean (true if included in distance calculation)
 *     source: id of a gold node
 *     target: id of a candidate node
 *   }
 * }
 */
vis.createClusterVis = function(graph) {
  var outersvg = document.createElementNS(d3.ns.prefix.svg, 'svg');
  var svg = document.createElementNS(d3.ns.prefix.svg, 'g');
  outersvg.appendChild(svg);

  /** Parameters */
  var width = 900,
      // height is computed later
      radius = 8,
      textLength = 50,
      titleHeight = 30;

  var maxTuples = 0, maxId = 0;
  graph.nodes.forEach(function(node) {
    if (maxTuples < node.reference.tuples.length) {
      maxTuples = node.reference.tuples.length;
    }
    if (maxId < node.id) {
      maxId = node.id;
    }
  });
  var maxRadius = radius * Math.sqrt(maxTuples) + 5;

  var edgeId = function(edgeIndex) {
    return 'edge_' + edgeIndex;
  };

  var lines = [];

  /** Scales */
  var color = d3.scale.category10();
  var ids = {'gold': 0, 'candidate': 1};
  var x = d3.scale.ordinal()
                  // Add a redundant 'worker' value to make rendering the
                  // category labels easier.
                  .domain(['gold', 'candidate', 'worker'])
                  .range([300, 500, 500]);
  var y = d3.scale.linear()
            .domain([0, maxId])
            .range([titleHeight + maxRadius,
                    titleHeight + 2*maxRadius*maxId]);
  var lineWidth = d3.scale.linear()
                    .domain([0,1])
                    .range([4, 1]);
  var height = y(maxId) + maxRadius;

  d3.select(outersvg).attr('width', width).attr('height', height);

  var positionLabel = function(theContainer) {
    var mousePos = d3.mouse(theContainer);
    var label = $('.edge-label', theContainer)[0];
    d3.select(label).attr('dx', mousePos[0]).attr('dy', mousePos[1]);
  };

  /** Category labels (e.g., 'gold' and 'worker') */
  d3.select(svg).selectAll('.category-label')
    .data(['gold', 'worker'])
  .enter().append('text')
  .classed('category-label', true)
  .attr('dx', function(d) { return x(d); })
  .attr('dy', titleHeight / 2 + 8)
  .attr('text-anchor', 'middle')
  .attr('stroke', 'black')
  .attr('font-size', 16)
  .text(function(d) { return d; });

  var edgeGroups = d3.select(svg).selectAll('.edge')
    .data(graph.edges)
  .enter().append('g');
 
  var lines = edgeGroups.append('line')
    .attr('class', 'edge')
    .attr('x1', function(e) { return x('gold'); })
    .attr('y1', function(e) { return y(e.source); })
    .attr('x2', function(e) { return x('candidate'); })
    .attr('y2', function(e) { return y(e.target); })
    .attr('stroke', function(e) {
      return e.min ? 'black' : '#ddd';}
    )
    .attr('stroke-width', function(e) { return lineWidth(e.distance); });
  
  var lineLabels = edgeGroups.append('text')
      .attr('class', 'edge-label')
      .style('display', 'none')
      .attr('id', function(e, index) { return edgeId(index); })
      .attr('dx', function(e) { return (x('gold') + x('candidate')) / 2; })
      .attr('dy', function(e) { return (y(e.source) + y(e.target)) / 2; })
      .attr('stroke', function(e) {
        return e.min ? 'black' : '#ddd';}
      )
      .text(function(e) { return e.distance.toPrecision(2); });

  edgeGroups.on('mouseover', function(e) {
    $('.edge-label', this).show();
    positionLabel(this);
    var line = $('.edge', this)[0];
    lines.attr('opacity', function(d) {
      return this === line ? 1 : 0.4;
    });
  })
  .on('mousemove', function(e) {
    positionLabel(this); })
  .on('mouseout', function(e) {
    $('.edge-label', this).hide();
    lines.attr('opacity', 1);
  })

  d3.select(svg).selectAll('.node')
    .data(graph.nodes)
  .enter().append('circle')
    .attr('class', 'node')
    .attr('r', function(d) {
      return radius * Math.sqrt(d.reference.tuples.length);
    })
    .style('fill', function(d) { return color(ids[d.group]); })
    .attr('cx', function(d) { return x(d.group); })
    .attr('cy', function(d) { return y(d.id); });

  d3.select(svg).selectAll('.node-label')
    .data(graph.nodes)
  .enter().append('text')
    .attr('class', 'node-label')
    .attr('dx', function(d) {
      var curX = x(d.group);
      return d.group === 'gold' ? curX-15 : curX+15;
    })
    .attr('dy', function(d) { return y(d.id) + 4; })
    .attr('text-anchor', function(d) {
      return d.group === 'gold' ? 'end' : 'start';
    })
    .text(function(d) {
      return vis.utils.getTextFromPhraseIndices(
        d.reference.text, d.reference.phrases, textLength);
    });

  d3.select(svg).selectAll('.node-tuple-label')
    .data(graph.nodes)
  .enter().append('text')
    .attr('class', 'node-tuple-label')
    .attr('dx', function(d) { return x(d.group); })
    .attr('dy', function(d) { return y(d.id)+4; })
    .attr('opacity', 0.5)
    .attr('text-anchor', 'middle')
    .text(function(d) { return d.reference.tuples.length; });

  var container = document.createElement('div');
  var buttonContainer = document.createElement('div');

  var radioButtons = ['Overall', 'Phrase distance', 'Tuple distance'];
  var radioButtonValues = ['distance', 'phrase_distance', 'tuple_distance'];
  var rblength = radioButtons.length;
  for (var i=0; i<rblength; i++) {
    var currentButtonHTML = '<input type="radio" name="distanceRadios" id="'+
      radioButtons[i]+'Radio'+'" value="'+
      radioButtonValues[i]+'"';
    if (i == 0) {
      currentButtonHTML += ' checked>';
    } else {
      currentButtonHTML += '>';
    }
    var currentButton = $(currentButtonHTML);
    currentButton.on('click', function() {
      console.log(this);
      console.log($(this));
      if ($(this).attr('checked')) {
        console.log($(this).val());
        updateLineWeights($(this).val());
      }
    });

    var radioButton = $('<label class="radio inline">').append(
      currentButton);
    radioButton.append($('<span>').text(radioButtons[i]));
    $(buttonContainer).append(radioButton);
  }

  var updateLineWeights = function(distanceType) {
    lines.attr('stroke-width', function(e) {
      console.log(e);
      return lineWidth(e[distanceType]);
    });
    lineLabels.text(function(e) {
      return e[distanceType].toPrecision(2);
    });
  };

  $(container).append(buttonContainer).append(outersvg);

  return container;
};
