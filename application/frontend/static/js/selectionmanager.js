(function(window, document) {

  var handlers = {
    'mouseover': function() {
      return function(event) {
          this.style.border = 'dashed 1px black';
          this.style.cursor = 'pointer';
      };
    },
    'mouseout': function() {
      return function(event) {
          this.style.border = 'none';
      };
    },
    'click': function(thisSelectionManager) {
      return function(event) {
        thisSelectionManager.paragraph.insertBefore(
          document.createTextNode(this.textContent), this);
        thisSelectionManager.paragraph.removeChild(this);
        SelectionManager.utils.mergeTextNodes(thisSelectionManager.paragraph);
      };
    }
  };

	var SelectionManager = function(textContainer, paragraph, text) {
    if(!paragraph) {
      this.paragraph = textContainer.querySelector('#theParagraph');
    } else {
      this.paragraph = paragraph;
    }
    if (text) {
      this.text = text;
    } else {
		  this.text = this.paragraph.innerHTML;
    }
	};

	SelectionManager.utils = {
		lca: function(n1, n2) {
			var getParents = function(n) {
				if(!n.parentNode) return [];
				return [n.parentNode].concat(getParents(n.parentNode));
			},
			n1parents = getParents(n1),
			curN2Parent = n2.parentNode;

			while(curN2Parent && n1parents.indexOf(curN2Parent) === -1) {
				curN2Parent = curN2Parent.parentNode;
			}

			return curN2Parent;
		},

		isAncestor: function(child, queryAncestor) {
			if(!child.parentNode) return false;
			if(child.parentNode === queryAncestor) return true;

			return this.isAncestor(child.parentNode, queryAncestor);
		},

		isDescendant: function(queryNode, parentNode) {
			if(!parentNode) return false;
			if(queryNode === parentNode) return true;

			for(var node in parentNode.childNodes) {
				if(this.isDescendant(queryNode, parentNode.childNodes[node])) return true;
			}

			return false;
		},

		mergeTextNodes: function(parent) {
			var i=0;
			while(i < parent.childNodes.length-1) {
				if(parent.childNodes[i].nodeType === Node.TEXT_NODE &&
				   parent.childNodes[i+1].nodeType === Node.TEXT_NODE) {
					parent.childNodes[i].textContent += parent.childNodes[i+1].textContent;
					parent.removeChild(parent.childNodes[i+1]);
				} else {
					i++;
				}
			}
		},
		
		// Code from http://stackoverflow.com/questions/6190143/javascript-set-window-selection
		clearSelection: function() {
			if(window.getSelection) { // Gecko, Mozilla
				window.getSelection().removeAllRanges();
			} else if(document.selection) { // IE < 9
				document.selection.empty();
			}
		}
	};
			
	SelectionManager.prototype = {
		SPAN: "__span__",
		constructor: SelectionManager,
		createSpan: function(text) {
			var thisSelectionManager = this;
			var newSpan = document.createElement('span');
			newSpan.setAttribute('class', 'selection');
			newSpan.innerHTML = text;
      var thisHandlers = {
          'mouseover': handlers.mouseover(),
          'mouseout': handlers.mouseout(),
          'click': handlers.click(thisSelectionManager)
      };
      newSpan.addEventListener('mouseover', thisHandlers.mouseover);
      newSpan.addEventListener('mouseout', thisHandlers.mouseout);
      newSpan.addEventListener('click', thisHandlers.click);
      newSpan['__handlers__'] = thisHandlers;
   			
			return newSpan;
		},
    removeInteraction: function() {
      var spans = this.paragraph.querySelectorAll('span');
      for(var i=0; i<spans.length; i++) {
        for(var handler in spans[i]['__handlers__']) {
          if(spans[i]['__handlers__'].hasOwnProperty(handler)) {
            spans[i].removeEventListener(handler, spans[i]['__handlers__'][handler]);
          }
        }
      }
    },
		updateSelection: function() {
			var selection = window.getSelection(),
				firstNode = null, firstOffset = 0, firstNodeLCAChild = 0,
				endNode = null, endOffset = 0, endNodeLCAChild = 0,
				currentText = this.paragraph.innerHTML;
			
			// The paragraph isn't a common ancestor of the selection nodes
			if(!SelectionManager.utils.isAncestor(selection.anchorNode, this.paragraph) ||
			   !SelectionManager.utils.isAncestor(selection.focusNode, this.paragraph)) {
				console.log('invalid selection');
				// Clear the selection
				SelectionManager.utils.clearSelection();
			}

			// There was no selection
			if(selection.anchorNode === selection.focusNode &&
				selection.anchorOffset === selection.focusOffset) return;

			// Find the least common ancestor
			//var lca = utils.lca(selection.anchorNode, selection.focusNode);
			// The paragraph is guaranteed to be the least common ancestor
			var lca = this.paragraph;
			
			// Determine which of the anchor and focus nodes is the first node
			// (i.e., the earlier child of the paragraph node)
			for(var i=0; i<lca.childNodes.length; i++) {
				if(SelectionManager.utils.isDescendant(selection.anchorNode, lca.childNodes[i])) {
					if(!firstNode) {
						firstNode = selection.anchorNode;
						firstOffset = selection.anchorOffset;
						firstNodeLCAChild = lca.childNodes[i];
						endNode = selection.focusNode;
						endOffset = selection.focusOffset;
					}
					else {
						endNodeLCAChild = lca.childNodes[i];
					}
				}
				
				if(SelectionManager.utils.isDescendant(selection.focusNode, lca.childNodes[i])) {
					if(!firstNode) {
						firstNode = selection.focusNode;
						firstOffset = selection.focusOffset;
						firstNodeChildIndex = i;
						firstNodeLCAChild = lca.childNodes[i];
						endNode = selection.anchorNode;
						endOffset = selection.anchorOffset;
					}
					else {
						endNodeLCAChild = lca.childNodes[i];
					}
				}
			}
			if(firstNode === endNode) {
				if(firstOffset > endOffset) {
					var temp = firstOffset;
					firstOffset = endOffset;
					endOffset = temp;
				}
			}

			var preText = firstNode.textContent.substring(0, firstOffset);
			var postText = endNode.textContent.substring(endOffset, endNode.textContent.length);
			var newText = "", newSpan, preTextNode, postTextNode;
			
			var startIndex = firstNodeLCAChild.previousSibling ? firstNodeLCAChild.previousSibling[this.SPAN].start : 0;				
			// If both anchor and focus nodes are the same node, then just replace
			// them with a span
			if(firstNode === endNode) {
				newText = firstNode.textContent.substring(firstOffset, endOffset);
				
				preTextNode = document.createTextNode(preText);					
				newSpan = this.createSpan(newText);
				postTextNode = document.createTextNode(postText);				
				
				lca.insertBefore(preTextNode, firstNodeLCAChild);
				lca.insertBefore(newSpan, firstNodeLCAChild);
				lca.insertBefore(postTextNode, firstNodeLCAChild);
				
				lca.removeChild(firstNodeLCAChild);
			}
			// If they are different, remove any overlapping spans and replace them with a new span
			else {
				/* Find the text in the highlighted region. The text spans multiple nodes. */
				newText = firstNode.textContent.substring(firstOffset, firstNode.length);
				var nextNode = firstNodeLCAChild.nextSibling, curNode = null;
				// Build up the text by checking each sibling in turn between the
				// start node and end node. Remove the siblings once we've extracted their text.
				while(nextNode && nextNode !== endNodeLCAChild) {
					newText += nextNode.textContent;
					curNode = nextNode;
					nextNode = nextNode.nextSibling;
					lca.removeChild(curNode);
				}
				newText += endNode.textContent.substring(0, endOffset);
				
				// Create text nodes to hold the leftover text
				preTextNode = document.createTextNode(preText);
				postTextNode = document.createTextNode(postText);
				
				// Create the new highlighted span
				newSpan = this.createSpan(newText);
				
				// Insert the new nodes in the right places
				lca.insertBefore(preTextNode, firstNodeLCAChild);
				lca.insertBefore(newSpan, firstNodeLCAChild);
				lca.insertBefore(postTextNode, firstNodeLCAChild);
				
				// Remove redundant nodes
				lca.removeChild(firstNodeLCAChild);
				lca.removeChild(endNodeLCAChild);
			}
			
			// Merge contiguous text nodes
			SelectionManager.utils.mergeTextNodes(lca);
			
			// Recalculate spans
			var curStart = 0;
			for(var i=0; i<lca.childNodes.length; i++) {
				lca.childNodes[i][this.SPAN] = {
					start: curStart,
					end: curStart + lca.childNodes[i].textContent.length
				}
				curStart = lca.childNodes[i][this.SPAN].end;
			}
		},
		removeSelections: function() {
			var spans = this.paragraph.getElementsByTagName('span');
			// Note that spans is a live updating NodeList -- it changes when the DOM structure changes
			while(spans.length > 0) {
				this.paragraph.insertBefore(
          document.createTextNode(spans[0].textContent), spans[0]);
				this.paragraph.removeChild(spans[0]);
			}
			SelectionManager.utils.mergeTextNodes(this.paragraph);
		},
		setSelections: function(selections) {
			// Sort the input selections in descending order
			selections.sort(function(a,b) {
				return b.end-a.end;
			});
			
			// Check if the selections are valid
			if(selections[selections.length-1].end > this.text.length) {
        selections[selections.length-1].end = this.text.length;
      }
			
			this.removeSelections();
			
			var currentTextNode = this.paragraph.childNodes[0];
      var postTextNode = null;
			for (var i=0; i<selections.length; i++) {
				postTextNode = null;
				if(selections[i].end < currentTextNode.textContent.length) {
					postTextNode = document.createTextNode(
            currentTextNode.textContent.substring(selections[i].end));
				}
				var spanNode = this.createSpan(
          currentTextNode.textContent.substring(
            selections[i].start, selections[i].end));
				
				if(this.paragraph.childNodes.length === 1) {
					this.paragraph.appendChild(spanNode);
					if(postTextNode) {
						this.paragraph.appendChild(postTextNode);
					}
				} else {	
					if(postTextNode) {
						this.paragraph.insertBefore(postTextNode, this.paragraph.childNodes[1]);
					}
					this.paragraph.insertBefore(spanNode, this.paragraph.childNodes[1]);
				}
				
				currentTextNode.textContent =
          currentTextNode.textContent.substr(0, selections[i].start);
			}

			// Re-sort in ascending order
			selections.sort(function(a,b) {
				return a.end-b.end;
			});
		}
	};
	
	window.SelectionManager = SelectionManager;
})( window, window.document );
