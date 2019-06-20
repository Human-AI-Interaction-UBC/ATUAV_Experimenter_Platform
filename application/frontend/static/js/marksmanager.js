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
	            })
							.sort(function(a,b) {
								return a.id - b.id;
							});
						console.log(marks);
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
							.duration(transition_out)
							.attr('fill-opacity', desat? DESATURATION: 0)
							.attr('stroke-width', 0) //Enamul: to remove Bolding Intervention
							.each('end', function() {
								d3.select(this).classed('selected', 'false');
							});
						d3.select(this.overlay).selectAll( '.arrow_selectArrow').remove();
					},
					"highlight": function(tuple_ids, reference_id, transition_in, args) {
						console.log("desaturate - highlight")
						var self = this,
							marks = self.getSelectedMarks(tuple_ids);  //used for desat
							selected_mark = self.getSelectedMarks([reference_id]); //used for bolding
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
							//console.log("dash_value:", args.dash);
							//var dash = "0, 0"
							//if (args.dash) dash = "12, 4"

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
									//.attr('stroke-dasharray', (dash))
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

    MarksManager.prototype.clusterLines = function(transition_in, id, tuple_ids, text_intervention_args){
        let self = this;
        let relativeCoords = {};
        let ref = document.getElementById('refAOI');
        let refRect = ref.getBoundingClientRect();
        let refParentRect = document.getElementById('textVisContainer').getBoundingClientRect();
        relativeCoords.refTop = refRect.top - refParentRect.top;
        relativeCoords.refLeft = refRect.left - refParentRect.left;

        let marks = self.getSelectedMarks(tuple_ids);
        let markRects = marks.selected_marks.map((mark) => {
        	return mark.getBoundingClientRect();
		});
        // markRects.sort((prev, cur) => {
        // 	return prev.x === cur.x ? prev.y - cur.y : prev.x - cur.x;
		// });
        let curCluster = [];
        let prevMarkRect = markRects[0];
        curCluster.push(prevMarkRect);
        for (let i = 1; i < markRects.length; i++) {
            let curMarkRect = markRects[i];
            let isShared = getSharedAxis(curCluster.concat(curMarkRect), 10).isShared;
            let sharedAxis = getSharedAxis(curCluster, 10);

            if (sharedAxis.hasOwnProperty('coord')) {
                if (sharedAxis.axis === 'x') {
                    relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                    relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
                } else {
                    relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                    relativeCoords.marky = sharedAxis.coord - refParentRect.top;
                }
            }

            if (!areMarksAdjacent(prevMarkRect, curMarkRect, 20) || !isShared) {
                self.strokeWidth = 1;
                if (curCluster.length === 1) {
                	if (prevMarkRect.width > prevMarkRect.height) {
                        relativeCoords.markx = prevMarkRect.left - refParentRect.left;
                        relativeCoords.marky = prevMarkRect.top - refParentRect.top + prevMarkRect.height / 2;
					} else {
                        relativeCoords.markx = prevMarkRect.left - refParentRect.left + prevMarkRect.width / 2;
                        relativeCoords.marky = prevMarkRect.top - refParentRect.top + prevMarkRect.height;
					}
                }

                d3.select(self.textVisOverlay).append("line")
                    .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                    .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                    .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
                    .style("stroke", text_intervention_args.link_colour)
                    .style("opacity", 0)
                    .style("stroke-width", self.strokeWidth)
                    .transition()
                    .duration(transition_in)
                    .style("opacity", 1);
                curCluster = [];
            }
            curCluster.push(curMarkRect);
            prevMarkRect = curMarkRect;
        }
        if (curCluster.length > 0) {
            let sharedAxis = getSharedAxis(curCluster, 10);

            if (curCluster.length === 1) {
            	let curMark = curCluster[0];
            	if (curMark.width > curMark.height) {
                    relativeCoords.markx = curMark.left - refParentRect.left;
                    relativeCoords.marky = curMark.top - refParentRect.top + curMark.height / 2;
				} else {
                    relativeCoords.markx = curMark.left - refParentRect.left + curMark.width / 2;
                    relativeCoords.marky = curMark.top - refParentRect.top + curMark.height;
				}

            } else if (sharedAxis.hasOwnProperty('coord')) {
                if (sharedAxis.axis === 'x') {
                    relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                    relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
                } else {
                    relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                    relativeCoords.marky = sharedAxis.coord - refParentRect.top;
                }
            }
            
            d3.select(self.textVisOverlay).append("line")
                .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
                .style("stroke", text_intervention_args.link_colour)
                .style("opacity", 0)
                .style("stroke-width", self.strokeWidth)
                .transition()
                .duration(transition_in)
                .style("opacity", 1);
        }
    };

    function areMarksAdjacent (prevMark, curMark, threshold) {
    	return Math.abs(prevMark.top - curMark.bottom) < threshold || Math.abs(prevMark.bottom - curMark.top) < threshold ||
			Math.abs(prevMark.left - curMark.right) < threshold || Math.abs(prevMark.right - curMark.left) < threshold;
	}

	function getSharedAxis(cluster, threshold) {
    	let shared = {};

    	if (cluster.length < 2) {
    		shared.isShared = true;
    		return shared;
		}

    	let prev = cluster[0];
    	for (let i = 1; i < cluster.length; i++) {
    		let cur = cluster[i];

    		if (shared.hasOwnProperty('axis')) {
    			if (shared.axis === 'x') {
                    shared.min = Math.min(cur.top, shared.min);
                    shared.max = Math.max(cur.bottom, shared.max);
    				if (!(Math.abs(prev.left - cur.left) < threshold || Math.abs(prev.right - cur.right) < threshold)) {
    					// NO shared axis
						shared.isShared = false;
						return shared;
					}
				} else if (shared.axis === 'y') {
                    shared.min = Math.min(cur.left, shared.min);
                    shared.max = Math.max(cur.right, shared.max);
                    if (!(Math.abs(prev.top - cur.top) < threshold || Math.abs(prev.bottom - cur.bottom) < threshold)) {
                        // NO shared axis
                        shared.isShared = false;
                        return shared;
                    }
				}
			} else {
                if (Math.abs(cur.top - prev.top) < threshold) {
                    shared.coord = cur.top;
                    shared.axis = 'y';
                    shared.min = Math.min(cur.left, prev.left);
                    shared.max = Math.max(cur.right, prev.right);
                } else if (Math.abs(cur.bottom - prev.bottom) < threshold) {
                    shared.coord = cur.bottom;
                    shared.axis = 'y';
                    shared.min = Math.min(cur.left, prev.left);
                    shared.max = Math.max(cur.right, prev.right);
                } else if (Math.abs(cur.left - prev.left) < threshold) {
                    shared.coord = cur.left;
                    shared.axis = 'x';
                    shared.min = Math.min(cur.top, prev.top);
                    shared.max = Math.max(cur.bottom, prev.bottom);
                } else if (Math.abs(cur.right - prev.right) < threshold) {
                    shared.coord = cur.right;
                    shared.axis = 'x';
                    shared.min = Math.min(cur.top, prev.top);
                    shared.max = Math.max(cur.bottom, prev.bottom);
                } else {
                	// NO shared axis
                    shared.isShared = false;
                    return shared;
				}
			}
			prev = cur;
		}

		shared.isShared = true;
		return shared;
	}


    MarksManager.prototype.clusterBranch = function(transition_in, id, tuple_ids, text_intervention_args){
        let self = this;
        let relativeCoords = {};
        let ref = document.getElementById('refAOI');
        let refRect = ref.getBoundingClientRect();
        let refParentRect = document.getElementById('textVisContainer').getBoundingClientRect();
        relativeCoords.refTop = refRect.top - refParentRect.top;
        relativeCoords.refLeft = refRect.left - refParentRect.left;

        let marks = self.getSelectedMarks(tuple_ids);
        let markRects = marks.selected_marks.map((mark) => {
            return mark.getBoundingClientRect();
        });
        // markRects.sort((prev, cur) => {
        // 	return prev.x === cur.x ? prev.y - cur.y : prev.x - cur.x;
        // });
        let curCluster = [];
        let prevMarkRect = markRects[0];
        curCluster.push(prevMarkRect);
        for (let i = 1; i < markRects.length; i++) {
            let curMarkRect = markRects[i];
            let isShared = getSharedAxis(curCluster.concat(curMarkRect), 10).isShared;
            let sharedAxis = getSharedAxis(curCluster, 10);

            if (sharedAxis.hasOwnProperty('coord')) {
                if (sharedAxis.axis === 'x') {
                    relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                    relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
                } else {
                    relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                    relativeCoords.marky = sharedAxis.coord - refParentRect.top;
                }
            }

            if (!areMarksAdjacent(prevMarkRect, curMarkRect, 20) || !isShared) {
                self.strokeWidth = 1;
                if (curCluster.length === 1) {
                    if (prevMarkRect.width > prevMarkRect.height) {
                        relativeCoords.markx = prevMarkRect.left - refParentRect.left;
                        relativeCoords.marky = prevMarkRect.top - refParentRect.top + prevMarkRect.height / 2;
                    } else {
                        relativeCoords.markx = prevMarkRect.left - refParentRect.left + prevMarkRect.width / 2;
                        relativeCoords.marky = prevMarkRect.top - refParentRect.top + prevMarkRect.height;
                    }
                }
                if (curCluster.length > 1) {
                	let xDiff = relativeCoords.markx - relativeCoords.refLeft;
                	relativeCoords.markx = relativeCoords.refLeft + 0.3 * xDiff;
                    let yDiff = relativeCoords.marky - relativeCoords.refTop;
                    relativeCoords.marky = relativeCoords.refTop + 0.3 * yDiff;
				}

                d3.select(self.textVisOverlay).append("line")
                    .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                    .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                    .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
                    .style("stroke", text_intervention_args.link_colour)
                    .style("opacity", 0)
                    .style("stroke-width", self.strokeWidth)
                    .transition()
                    .duration(transition_in)
                    .style("opacity", 1);

                if (curCluster.length > 1) {
                	for (let i = 0; i < curCluster.length; i++) {
                		let markX = curCluster[i].left;
                		let markY = curCluster[i].top;
                        if (curCluster[i].width > curCluster[i].height) {
                            markX = curCluster[i].left - refParentRect.left;
                            markY = curCluster[i].top - refParentRect.top + curCluster[i].height / 2;
                        } else {
                            markX = curCluster[i].left - refParentRect.left + curCluster[i].width / 2;
                            markY = curCluster[i].top - refParentRect.top + curCluster[i].height;
                        }
                        d3.select(self.textVisOverlay).append("line")
                            .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                            .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                            .attr("x1", markX).attr("y1", markY)
                            .style("stroke", text_intervention_args.link_colour)
                            .style("opacity", 0)
                            .style("stroke-width", self.strokeWidth)
                            .transition()
                            .duration(transition_in)
                            .style("opacity", 1);
					}
				}
                curCluster = [];
            }
            curCluster.push(curMarkRect);
            prevMarkRect = curMarkRect;
        }
        if (curCluster.length > 0) {
            let sharedAxis = getSharedAxis(curCluster, 10);

            if (curCluster.length === 1) {
                let curMark = curCluster[0];
                if (curMark.width > curMark.height) {
                    relativeCoords.markx = curMark.left - refParentRect.left;
                    relativeCoords.marky = curMark.top - refParentRect.top + curMark.height / 2;
                } else {
                    relativeCoords.markx = curMark.left - refParentRect.left + curMark.width / 2;
                    relativeCoords.marky = curMark.top - refParentRect.top + curMark.height;
                }

            } else if (sharedAxis.hasOwnProperty('coord')) {
                if (sharedAxis.axis === 'x') {
                    relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                    relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
                } else {
                    relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                    relativeCoords.marky = sharedAxis.coord - refParentRect.top;
                }
            }

            if (curCluster.length > 1) {
                let xDiff = relativeCoords.markx - relativeCoords.refLeft;
                relativeCoords.markx = relativeCoords.refLeft + 0.3 * xDiff;
                let yDiff = relativeCoords.marky - relativeCoords.refTop;
                relativeCoords.marky = relativeCoords.refTop + 0.3 * yDiff;
            }

            d3.select(self.textVisOverlay).append("line")
                .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
                .style("stroke", text_intervention_args.link_colour)
                .style("opacity", 0)
                .style("stroke-width", self.strokeWidth)
                .transition()
                .duration(transition_in)
                .style("opacity", 1);

            if (curCluster.length > 1) {
                for (let i = 0; i < curCluster.length; i++) {
                    let markX = curCluster[i].left;
                    let markY = curCluster[i].top;
                    if (curCluster[i].width > curCluster[i].height) {
                        markX = curCluster[i].left - refParentRect.left;
                        markY = curCluster[i].top - refParentRect.top + curCluster[i].height / 2;
                    } else {
                        markX = curCluster[i].left - refParentRect.left + curCluster[i].width / 2;
                        markY = curCluster[i].top - refParentRect.top + curCluster[i].height;
                    }
                    d3.select(self.textVisOverlay).append("line")
                        .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                        .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                        .attr("x1", markX).attr("y1", markY)
                        .style("stroke", text_intervention_args.link_colour)
                        .style("opacity", 0)
                        .style("stroke-width", self.strokeWidth)
                        .transition()
                        .duration(transition_in)
                        .style("opacity", 1);
                }
            }
        }
    };


    MarksManager.prototype.drawMidLine = function(transition_in, id, tuple_ids, text_intervention_args){
        let self = this;
        let relativeCoords = {};
        let ref = document.getElementById('refAOI');
        let refRect = ref.getBoundingClientRect();
        let refParentRect = document.getElementById('textVisContainer').getBoundingClientRect();
        relativeCoords.refTop = refRect.top - refParentRect.top;
        relativeCoords.refLeft = refRect.left - refParentRect.left;

        let marks = self.getSelectedMarks(tuple_ids);
        let markRects = marks.selected_marks.map((mark) => {
            return mark.getBoundingClientRect();
        });
        // markRects.sort((prev, cur) => {
        // 	return prev.x === cur.x ? prev.y - cur.y : prev.x - cur.x;
        // });
            let sharedAxis = getSharedAxis(markRects, 10);
            if (sharedAxis.hasOwnProperty('coord')) {
                if (sharedAxis.axis === 'x') {
                    relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                    relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
                } else {
                    relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                    relativeCoords.marky = sharedAxis.coord - refParentRect.top;
                }
            } else {
            	// assuming that any marks with no shared axis are probably horizontal bars
				let minY = markRects[0].top;
				let maxY = markRects[0].bottom;
				let left = markRects[0].left;

				markRects.forEach((mark) => {
					minY = Math.min(minY, mark.top);
					maxY = Math.max(maxY, mark.bottom);
					left = Math.min(left, mark.left);
				});
				relativeCoords.markx = left - refParentRect.left;
				relativeCoords.marky = (minY + maxY) / 2 - refParentRect.top;
			}

            d3.select(self.textVisOverlay).append("line")
                .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
                .style("stroke", text_intervention_args.link_colour)
                .style("opacity", 0)
                .style("stroke-width", self.strokeWidth)
                .transition()
                .duration(transition_in)
                .style("opacity", 1);
    };

    MarksManager.prototype.midLineBranch = function(transition_in, id, tuple_ids, text_intervention_args){
        let self = this;
        let relativeCoords = {};
        let ref = document.getElementById('refAOI');
        let refRect = ref.getBoundingClientRect();
        let refParentRect = document.getElementById('textVisContainer').getBoundingClientRect();
        relativeCoords.refTop = refRect.top - refParentRect.top;
        relativeCoords.refLeft = refRect.left - refParentRect.left;

        let marks = self.getSelectedMarks(tuple_ids);
        let markRects = marks.selected_marks.map((mark) => {
            return mark.getBoundingClientRect();
        });
        // markRects.sort((prev, cur) => {
        // 	return prev.x === cur.x ? prev.y - cur.y : prev.x - cur.x;
        // });
        let sharedAxis = getSharedAxis(markRects, 10);
        if (sharedAxis.hasOwnProperty('coord')) {
            if (sharedAxis.axis === 'x') {
                relativeCoords.markx = sharedAxis.coord - refParentRect.left;
                relativeCoords.marky = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.top;
            } else {
                relativeCoords.markx = (sharedAxis.min + sharedAxis.max) / 2 - refParentRect.left;
                relativeCoords.marky = sharedAxis.coord - refParentRect.top;
            }
        } else {
            // assuming that any marks with no shared axis are probably horizontal bars
            let minY = markRects[0].top;
            let maxY = markRects[0].bottom;
            let left = markRects[0].left;

            markRects.forEach((mark) => {
                minY = Math.min(minY, mark.top);
                maxY = Math.max(maxY, mark.bottom);
                left = Math.min(left, mark.left);
            });
            relativeCoords.markx = left - refParentRect.left;
            relativeCoords.marky = (minY + maxY) / 2 - refParentRect.top;
        }

        if (markRects.length > 1) {
            let xDiff = relativeCoords.markx - relativeCoords.refLeft;
            relativeCoords.markx = relativeCoords.refLeft + 0.3 * xDiff;
            let yDiff = relativeCoords.marky - relativeCoords.refTop;
            relativeCoords.marky = relativeCoords.refTop + 0.3 * yDiff;
        }

        d3.select(self.textVisOverlay).append("line")
            .attr("class", "line_" + id + " " + text_intervention_args.link_type)
            .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
            .attr("x1", relativeCoords.refLeft + refRect.width).attr("y1", relativeCoords.refTop + refRect.height / 2)
            .style("stroke", text_intervention_args.link_colour)
            .style("opacity", 0)
            .style("stroke-width", self.strokeWidth)
            .transition()
            .duration(transition_in)
            .style("opacity", 1);

        if (markRects.length > 1) {
            for (let i = 0; i < markRects.length; i++) {
                let markX = markRects[i].left;
                let markY = markRects[i].top;
                if (markRects[i].width > markRects[i].height) {
                    markX = markRects[i].left - refParentRect.left;
                    markY = markRects[i].top - refParentRect.top + markRects[i].height / 2;
                } else {
                    markX = markRects[i].left - refParentRect.left + markRects[i].width / 2;
                    markY = markRects[i].top - refParentRect.top + markRects[i].height;
                }
                d3.select(self.textVisOverlay).append("line")
                    .attr("class", "line_" + id + " " + text_intervention_args.link_type)
                    .attr("x2", relativeCoords.markx).attr("y2", relativeCoords.marky)
                    .attr("x1", markX).attr("y1", markY)
                    .style("stroke", text_intervention_args.link_colour)
                    .style("opacity", 0)
                    .style("stroke-width", self.strokeWidth)
                    .transition()
                    .duration(transition_in)
                    .style("opacity", 1);
            }
        }
    };

    MarksManager.prototype.drawBox = function(tuple_ids, reference_id, transition_in, args) {
        let self = this,
        selectedMarks = self.getSelectedMarks([reference_id]).selected_marks; //used for bolding
        let bold_thickness = args.bold_thickness || 1;
        let markRects = selectedMarks.map((mark) => {
            return mark.getBoundingClientRect();
        });

        let minY = markRects[0].top;
        let maxY = markRects[0].bottom;
        let minX = markRects[0].left;
        let maxX = markRects[0].right;

        markRects.forEach((mark) => {
            minY = Math.min(minY, mark.top);
            maxY = Math.max(maxY, mark.bottom);
            minX = Math.min(minX, mark.left);
            maxX = Math.max(maxX, mark.right);
        });

        d3.select(this.overlay).append('rect')
			.attr("x", minX)
			.attr("y", minY)
			.attr("width", maxX - minX)
			.attr("height", maxY - minY)
			.attr("stroke-width", bold_thickness)
			.attr("fill-opacity", 0)
			.style("opacity", 0)
            .transition()
            .duration(transition_in)
			.style("opacity", 1)
            .each('end', function() {
                d3.select(this).attr('id', 'reference_' + reference_id);
                d3.select(this).classed('selected', true);
            });
	};

    MarksManager.prototype.removeLines = function(tuple_id) {
    	d3.selectAll('.line_' + tuple_id).remove();
	};

    MarksManager.prototype.createTextVisOverlay = function(elem_id) {
        let textVisElement = document.getElementById(elem_id);
        let textVisCoords = textVisElement.getBoundingClientRect();
        let containingDiv = document.createElement('div');
        containingDiv.setAttribute('class','textVisOverlayContainer');
        containingDiv.setAttribute('id', 'textVisContainer');
        containingDiv.style.position = 'absolute';
        containingDiv.style.width = Math.ceil(textVisCoords.width)+'px';
        containingDiv.style.height = Math.ceil(textVisCoords.height)+'px';

        this.textVisOverlay = document.createElementNS("http://www.w3.org/2000/svg", 'svg:svg');
        d3.select(this.textVisOverlay).attr({
            "class": "textVisOverlay",
            'height': Math.ceil(textVisCoords.height),
            "width": Math.ceil(textVisCoords.width)
        }).style({
            'position': 'absolute'
        });

        containingDiv.appendChild(this.textVisOverlay);

        let parent = textVisElement.parentNode;
        let nextSibling = textVisElement.nextSibling;
        parent.insertBefore(containingDiv, nextSibling);
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
