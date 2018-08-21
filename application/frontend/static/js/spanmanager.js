(function(window, document){
	
	var SpanManager = function(paragraph) {
		this.paragraph = paragraph;
	};
	
	SpanManager.utils = {
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
	};
	
	SpanManager.defaultSpanCreator = function(text) {
		var newSpan = document.createElement('span');
		newSpan.textContent = text;
		return newSpan;
	};
	
	function clearSpans() {
		var spans = this.paragraph.getElementsByTagName('span');
		// Note that spans is a live updating NodeList -- it changes when the DOM structure changes
		while(spans.length > 0) {
			this.paragraph.insertBefore(document.createTextNode(spans[0].textContent), spans[0]);
			this.paragraph.removeChild(spans[0]);
		}
		SpanManager.utils.mergeTextNodes(this.paragraph);
	}
	
	/*
	 * Create spans in text using the spans given. Spans is an array
	 * of objects with start and end properties to the beginning and
	 * end indices of each span. 
	 */
	function createSpans(spans, spanCreatorFunc) {
		// Input check: make sure the input is of the right format
		spans.forEach(function(span, i) {
			if(!span.hasOwnProperty('start')) throw "No start value given in span " + i;
			if(!span.hasOwnProperty('end')) throw "No end value given in span " + i;
		});
		
		if(!spanCreatorFunc) spanCreatorFunc = SpanManager.defaultSpanCreator;
		else {
			spanCreatorFunc = (function(scf){
				return function(text, span) {
					var newSpan = SpanManager.defaultSpanCreator(text);
					scf.call(this, newSpan, span);
					return newSpan;
				};
			})(spanCreatorFunc);
		}
		
		// Sort the spans in descending order
		spans.sort(function(a,b) {
			return b.start-a.start;
		});
	
		// Clear any existing spans
		this.clearSpans();
		
		// Create the spans in descending order
		var newSpans = [];
		var currentTextNode = this.paragraph.childNodes[0];
        var postTextNode = null;
		for(var i=0; i<spans.length; i++) {
			postTextNode = null;
			if(spans[i].end < currentTextNode.textContent.length) {
				postTextNode = document.createTextNode(currentTextNode.textContent.substring(spans[i].end));
			}
			var spanNode = spanCreatorFunc.call(this, currentTextNode.textContent.substring(spans[i].start, spans[i].end), spans[i]);
			newSpans.push(spanNode);
			
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
			
			currentTextNode.textContent = currentTextNode.textContent.substr(0, spans[i].start);
		}
		
		// Reverse the spans so they are in the same order as the input phrases
		spans.sort(function(a,b) { return a.start - b.start; });
		var i=0, j=newSpans.length-1;
		while(i < j) {
			var temp = newSpans[i];
			newSpans[i] = newSpans[j];
			newSpans[j] = temp;
			i++; j--;
		}
		
		return newSpans;
	}
	
	SpanManager.prototype.createSpans = createSpans;
	SpanManager.prototype.clearSpans = clearSpans;
	
	window.SpanManager = SpanManager;
	
})(window, window.document);
