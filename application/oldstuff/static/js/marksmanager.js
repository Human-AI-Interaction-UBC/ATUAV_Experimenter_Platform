(function(){
	var MarksManager = function(marks, img) {
		this.data = marks;
		this.img = img;

		this.type = MarksManager.HIGHLIGHT;
		this.current_params = MarksManager.defaultHighlightParams;

		this.marks = [];

    this.scale = {
      x: 1,
      y: 1
    };
	};
	MarksManager.defaultHighlightParams = {
		'attributes': {
		},
		'style': {
			'display': 'block'
		},
		'classes': ['visual_reference']
	};
	MarksManager.defaultDesaturateParams = {
		'attributes': {
			'fill': 'white',
			'fill-opacity': 0
		},
		'style': {
			'display': 'block'
		},
		'classes': ['visual_reference']
	}
	MarksManager.HIGHLIGHT = "highlight";
	MarksManager.DESATURATE = "desaturate";

  var DESATURATION = 0.7;
	MarksManager.internal = {
		highlights: {
			"highlight": {
				"create": function() {
						var self = this;
						var marks = d3.select(self.overlay).selectAll('rect')
						  .data(self.data, function(d) { return d ? d.id : null; });

						marks.enter()
						  .append('rect').attr('x', function(d) { return d.left*self.scale.x; })
						  .attr('y', function(d) { return d.top*self.scale.y; })
						  .attr('width', function(d) { return d.width*self.scale.x; })
						  .attr('height', function(d) { return d.height*self.scale.y; });

						marks.exit().remove();
						console.log("highlight - create")
						return d3.select(self.overlay).selectAll('rect');
					},
					"highlight": function(tuple_ids) {
					console.log("highlight - highlight")
						//d3.selectAll(this.marks)
	            d3.select(this.overlay).selectAll('rect')
						  .style('display', function(mark_data) {
							  for(var i=0; i<tuple_ids.length; i++) {
							      if(tuple_ids[i] === mark_data.id) return 'block';
							  }
							  return 'none';
						  });
					},
					"unhighlight": function() {
						console.log("highlight - unhighlight")
	          d3.selectAll(this.marks).style('display', 'none');
	        }
			},
			"desaturate": {
					"create": function() {
						console.log("desaturate - create")
						var self = this;

						var margin = 1;
						var marks = d3.select(self.overlay).selectAll('rect')
						  .data(self.data, function(d) { return d.id; }).enter()
						  .append('rect')
	            .attr('x', function(d) {
	              return (d.left-margin)*self.scale.x;
	            })
						  .attr('y', function(d) {
	              return (d.top-margin)*self.scale.y;
	            })
						  .attr('width', function(d) {
	              return (d.width+margin*2)*self.scale.x;
	            })
						  .attr('height', function(d) {
	              return (d.height+margin*2)*self.scale.y;
	            })
	            .on('click._marksmanager', function(d) {
								if(!d3.select(this).classed('selected')) {
									MarksManager.internal.highlights['desaturate'].highlight.call(self, [d.id]);
								}
								else {
									MarksManager.internal.highlights['desaturate'].unhighlight.call(self);
								}
	            });
						// Extract only the marks that are mentioned
						var referenced_marks = self.data.reduce(function(acc, val) {
													if(val.tuple) acc.push(val);
													return acc;
												}, []);
						return marks[0];
						// var hints = d3.select(this.overlay).selectAll('circle')
						// 			  .data(referenced_marks, function(d) { return d.id; })
						// 			  .enter().append('circle')
						// 			  .attr('cx', function(d) { return d.left; })
						// 			  .attr('cy', function(d) { return d.top; })
						// 			  .attr('r', 3).attr('fill', 'red').attr('fill-opacity', 0.5)
						// 			  .classed('reference_hint', true);
					},
					"unhighlight": function(interventions, to_be_removed) {
						console.log("desaturate - unhighlight")
						var tuple_ids = Object.values(interventions).map(function(obj) {return obj.tuple_id});
						console.log("NEW TUPLE IDS")
						console.log(tuple_ids)
						var self = this,
							marks = self.getSelectedMarks(tuple_ids);
							console.log("removing: selected marks" + marks.selected_marks.length);
						/*d3.selectAll('.visual_reference')
							.transition()
							.attr('fill-opacity', 0)
							.duration(TRANSITION_DURATION);*/
						var desat = Object.values(interventions).map(function(obj) {return obj.args.desat}).includes(true); // true if there is an intervention with desat
						var transition_out = to_be_removed.transition_out || 0;
						d3.selectAll(marks.unselected_marks)
							.transition()
							.attr('fill-opacity', desat? DESATURATION: 0)
							.attr('stroke-width', 0) //Enamul: to remove Bolding Intervention
							.duration(transition_out)
							.each('end', function() {
								d3.select(this).classed('selected', 'false');
							});
						d3.select(this.overlay).selectAll( '.arrow_selectArrow').remove();
					},
					"highlight": function(tuple_ids, reference_id, transition_in, args) {
						console.log("desaturate - highlight")
						var self = this,
							marks = self.getSelectedMarks(tuple_ids);
							selected_mark = self.getSelectedMarks([reference_id]);
							console.log("tuple_ids " + tuple_ids);
							console.log("reference_id " + reference_id);
							console.log("args" + args);

							var transition_in = transition_in || 0; //TODO: maybe this should be TRANSITION_DURATION
							var color = args.color;
							var arrow = args.arrow;
							var arrow_direction = args.arrow_direction;
							var desat = args.desat;
							var bold = args.bold;
							var bold_thickness = args.bold_thickness || 1;

	            	/*if(arrow){
									self.arrowwidth = 25;
	                for(var i=0;i<marks.selected_marks.length;i++){
	                  var d3mark = d3.select(marks.selected_marks[i]);
	                  var mark_data = d3mark.data()[0];
	                  var arrowSize = Math.min(10, mark_data.height/2-2);
										if (arrow_direction == "top") {
												self.drawArrow(d3.select(this.overlay), mark_data.left+ mark_data.width/2,
																													mark_data.top - self.arrowwidth,
																													mark_data.left+ mark_data.width/2,
																													mark_data.top - 2, arrowSize, transition_in, 'selectArrow');
										} else if (arrow_direction == "bottom") {
												self.drawArrow(d3.select(this.overlay), mark_data.left+ mark_data.width/2,
																													mark_data.height + mark_data.top + self.arrowwidth,
																													mark_data.left+ mark_data.width/2,
																													mark_data.height + mark_data.top + 2, arrowSize, transition_in, 'selectArrow');
										} else if (arrow_direction == "left") {
												self.drawArrow(d3.select(this.overlay), mark_data.left - self.arrowwidth,
																													mark_data.height/2+ mark_data.top,
																													mark_data.left- 2,
																													mark_data.height/2+ mark_data.top, arrowSize, transition_in,  'selectArrow');
										} else {
												// default: arrow starts on the right side
	                  		self.drawArrow(d3.select(this.overlay), mark_data.left+ mark_data.width+self.arrowwidth,
																														mark_data.height/2+ mark_data.top,
																														mark_data.left+ mark_data.width+2,
																														mark_data.height/2+ mark_data.top, arrowSize, transition_in, 'selectArrow');
										}
	                }

								}
								else{ //TEST
									d3.select(this.overlay).selectAll( '.arrow_selectArrow')
											.transition()
											.duration(transition_in)
											.remove();

	              }*/

								/*d3.selectAll('.visual_reference')
									.sort( function(a, b) {
										if (marks.selected_marks.includes(a)) return 1;
										else return -1;
									});*/ //TODO: currently non functioning

	              d3.selectAll(selected_mark.selected_marks)
	                .attr('stroke', 'white')
									.attr('stroke-width', 0)
	                .transition()
	                .duration(transition_in)
	                //.attr('fill-opacity', 0)
								  .attr('stroke-width', bold_thickness)
	                .attr('stroke', function () { return bold? color: 'none';})
									.attr('fill-opacity', 0)
	                .each('end', function() {
	                  d3.select(this).attr('id', 'reference_' + reference_id);
										d3.select(this).classed('selected', true);
	                  //d3.select(this).classed('selected', !d3.select(this).classed('selected'));
	                });
	              d3.selectAll(marks.unselected_marks)
	                .transition()
	                .duration(transition_in)
									.attr('stroke-width', 0)
	                .attr('fill-opacity', function(mark_data) {
											//var this_selection = d3.select(this)[0];
											//console.log("contains? :" + marks.selected_marks.includes(this));
											//console.log(d3.select(this).attr("class"));
											//console.log(d3.select(this).property("className"));
											return marks.selected_marks.length === 0 ? 0 : desat? DESATURATION: 0;
	                });
					},
					"highlightLegend": function(transition_in, args) {
						var legend_mark = this.getLegendMark();
						var transition_in = transition_in || 0; //TODO: maybe this should be TRANSITION_DURATION
						var color = args.color;
						//var arrow = args.arrow;
						//var arrow_direction = args.arrow_direction; //TODO: no suppor for arrows or desat currently
						//var desat = args.desat;
						var bold = args.bold;
						var bold_thickness = args.bold_thickness || 1;
						console.log("highlighting legend");
						d3.select(legend_mark)
							.attr('stroke', 'white')
							.attr('stroke-width', 0)
							.transition()
							.attr('stroke-width', bold_thickness)
							.duration(transition_in)
							//.attr('fill-opacity', 0)
							.attr('stroke', function () { return bold? color: 'none';})
							.attr('fill-opacity', 0);

						console.log("highlighted legend")
					}
			}
		}
	};


  MarksManager.prototype.drawArrow = function(svgElement, x1, y1, x2, y2, size, transition_in, id){
    this.strokeWidth = 2;
    var angle = Math.atan2(x1 - x2, y2 - y1);
    angle = (angle / (2 * Math.PI)) * 360;
    svgElement.append("path")
        .attr("class", "arrow_" + id)
        .attr("d", "M" + x2 + " " + y2 + " L" + (x2 - size) + " " + (y2 - size) + " L" + (x2 - size) + " " + (y2 + size) + " L" + x2 + " " + y2)
        .attr("transform", "rotate(" + (90 + angle)+ "," + x2 + "," + y2 +")")
        .attr("fill", "black")
        .style("opacity", 0)
        .transition()
        .duration(transition_in)
        .style("opacity", 1)
    svgElement.append("svg:line")

        .attr("class", "arrow_"+id)
        .attr("x1", x1).attr("y1", y1)
        .attr("x2", x2).attr("y2", y2)
        .style("stroke", "black")
        .style("opacity", 0)
				.style("stroke-width", this.strokeWidth)
        .transition()
        .duration(transition_in)
        .style("opacity", 1);
  };
	MarksManager.prototype.changeType = function(type) {
		var marks;

		if(!type) type = MarksManager.DESATURATE;
		this.type = type;

		this.clearMarks();

		if(type === MarksManager.HIGHLIGHT) {
			this.current_params = MarksManager.defaultHighlightParams;
		}
		if(type === MarksManager.DESATURATE) {
			this.current_params = MarksManager.defaultDesaturateParams;
		}
		this.marks = MarksManager.internal.highlights[type].create.call(this);
		this.assignParams(this.current_params);
	};
	MarksManager.prototype.createOverlay = function(type, params) {
		if(!params) params = this.current_params;
		if(type) {
			this.type = type;
		}

		/*
		 * Create the overlay
		 */
		var svgns = "http://www.w3.org/2000/svg";

		// Create an svg overlay on the image
		var imgParent = this.img.parentNode,
			nextSibling = this.img.nextSibling,
			nodeRect = this.img.getBoundingClientRect(),
			containingDiv,
			marksOverlay;

		// Create the containing div
		containingDiv = document.createElement('div');
		containingDiv.setAttribute('class','overlayContainer');
		containingDiv.style.position = 'relative';
		containingDiv.style.width = Math.ceil(nodeRect.width)+'px';
		containingDiv.style.height = Math.ceil(nodeRect.height)+'px';

		// Create the overlay
		this.overlay = document.createElementNS(svgns, 'svg:svg');
		d3.select(this.overlay).attr({
			"class": "overlay",
			'height': Math.ceil(nodeRect.height),
			"width": Math.ceil(nodeRect.width)
		}).style({
			'position': 'absolute'
		});

		containingDiv.appendChild(this.overlay);
		containingDiv.appendChild(this.img);

		imgParent.insertBefore(containingDiv, nextSibling);

    // Set the scale
    this.scale.x = Math.ceil(nodeRect.width) / this.img.naturalWidth;
    this.scale.y = Math.ceil(nodeRect.height) / this.img.naturalHeight;

		// Overlay the marks
		this.current_params = params;
		this.update();
	};
  MarksManager.prototype.removeOverlay = function() {
    this.img.parentNode.parentNode.replaceChild(this.img, this.img.parentNode);
  };
	MarksManager.prototype.assignParams = function(params) {
		if(!this.overlay) throw "No overlay associated with this image."

		var marks = d3.select(this.overlay).selectAll('rect'),
			key;
		for(key in params.attributes) {
			if(params.attributes.hasOwnProperty(key)) {
				marks.attr(key, params.attributes[key]);
			}
		}
		for(key in params.style) {
			if(params.style.hasOwnProperty(key)) {
				marks.style(key, params.style[key]);
			}
		}
		params.classes.forEach(function(c) {
			marks.classed(c, true);
		});
	};
	MarksManager.prototype.getSelectedMarks = function(tuple_ids) {
		var self = this;
		var selected_marks = [],
			unselected_marks = [];
	 	for(var j=0; j<self.marks.length; j++) {
			(function(curMark) {
				var d3mark = d3.select(curMark);
				var mark_data = d3mark.data()[0];
				if (mark_data.id != "legend") {
					var selected = false;
		        	for(var i=0; i<tuple_ids.length; i++) {
									if(tuple_ids[i] === mark_data.id) {
										selected_marks.push(curMark);
										selected = true;
										return;
							}
					}
					if(!selected) unselected_marks.push(curMark);
				}
			})(self.marks[j]);
	    }

		return {
			'selected_marks': selected_marks,
			'unselected_marks': unselected_marks
		};
	};
	MarksManager.prototype.getLegendMark = function() {
		var self = this;
		for (var i=0; i<self.marks.length; i++){
				var d3mark = d3.select(self.marks[i]);
				console.log(d3mark)

				var mark_data = d3mark.data()[0];
				console.log(mark_data)

				if (mark_data.id == "legend") {
					return self.marks[i];
				}
		}
	};
	MarksManager.prototype.update = function() {
		this.marks = MarksManager.internal.highlights[this.type].create.call(this);
		this.assignParams(this.current_params);
	};
	MarksManager.prototype.highlight = function(tuple_ids, reference_id, transition_in, args) {
		MarksManager.internal.highlights[this.type].highlight.call(
        this, tuple_ids, reference_id, transition_in, args);
	};
	MarksManager.prototype.unhighlight = function(interventions, to_be_removed) {
		console.log("NEW TUPLE IDS")
		console.log()
		MarksManager.internal.highlights[this.type].unhighlight.call(this, interventions, to_be_removed);
	};
	MarksManager.prototype.highlightLegend = function(transition_in, args) {
		MarksManager.internal.highlights[this.type].highlightLegend.call(this, transition_in, args);
	};
	MarksManager.prototype.clearMarks = function() {
		d3.select(this.overlay).selectAll('.visual_reference').remove();
	};

	window.MarksManager = MarksManager;
})();
