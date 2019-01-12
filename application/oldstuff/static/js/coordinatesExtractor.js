/**
 * Created by enamul on 6/3/2017.
 */
function findCoordinatesofCharacters(textElementID) {
  var coordinatesChars = [];
  var newText =  "";
  var oldText = $(textElementID).text().trim();

  for (var i = 0, len = oldText.length; i < len; i++) {
    newText+= '<span>'+oldText[i]+ '</span>';
  }
  //console.log(newText);

  $(textElementID).html(newText);

  $spans = $(textElementID).find('span');
  $spans.each(function(){
    var $span = $(this),
        $offset = $span.offset();
    $offset.width = $span.innerWidth();
    $offset.height = $span.innerHeight();
    coordinatesChars.push($offset);
    //console.log($offset);
  });
  $(textElementID).html(oldText);
  return coordinatesChars;
}


function findCoordinatesofSentences(textElementID, coordinatesofChar) {
  var sentSpanCoord = [], sentencePolygonCoordinates = [];
  var newText =  "";
  var oldText = $(textElementID).text().trim();

  var result = oldText.match( /[^\.!\?]+[\.!\?]+/g ); // regular expression for splitting into sentences

  //put a span for each sentence
  for (var i = 0, len = result.length; i < len; i++) {
    newText+= '<span>'+result[i]+ '</span>';
  }
  $(textElementID).html(newText);

  $spans = $(textElementID).find('span');
  $spans.each(function(){
    var $span = $(this),
        $offset = $span.offset();
    $offset.width = $span.innerWidth();
    $offset.height = $span.innerHeight();
    $offset.sentence = $span.text();
    sentSpanCoord.push($offset);
    //console.log($offset);
  });
  $(textElementID).html(oldText); //get back to original text without spans
// loop over each sentence of the paragraph
  for(var i=0; i<sentSpanCoord.length;i++){
    var paragraphText = oldText;
    var sentenceStartPosition = paragraphText.indexOf(sentSpanCoord[i].sentence);
    var sentenceEndPosition = paragraphText.indexOf(sentSpanCoord[i].sentence)+sentSpanCoord[i].sentence.length-1;
    //console.log(sentenceStartPosition,sentenceEndPosition);
    var coordofSentStartPosition = coordinatesofChar[sentenceStartPosition];
    var coordofSentEndPosition = coordinatesofChar[sentenceEndPosition];

    // eight points needed to build the polygon
    sentencePolygonCoordinates.push(
      {sentence:sentSpanCoord[i].sentence, start:sentenceStartPosition, end: sentenceEndPosition,
      numofwords:sentSpanCoord[i].sentence.split(" ").length,
      polygonCoords:[
      {x:coordofSentStartPosition.left, y:coordofSentStartPosition.top},
      {x:coordofSentStartPosition.left, y:coordofSentStartPosition.top+coordofSentStartPosition.height},
      {x:sentSpanCoord[i].left, y:coordofSentStartPosition.top+coordofSentStartPosition.height},
      {x:sentSpanCoord[i].left, y:sentSpanCoord[i].top+ sentSpanCoord[i].height},
      {x:coordofSentEndPosition.left+coordofSentEndPosition.width, y:coordofSentEndPosition.top+coordofSentEndPosition.height},
      {x:coordofSentEndPosition.left+coordofSentEndPosition.width, y:coordofSentEndPosition.top},
      {x:sentSpanCoord[i].left + sentSpanCoord[i].width, y:coordofSentEndPosition.top},
      {x:sentSpanCoord[i].left + sentSpanCoord[i].width, y:sentSpanCoord[i].top}
    ]});
  }

  return sentencePolygonCoordinates;
};

function findCoordinatesofRefSentences(textElementID, coordinatesofChar, startEndCoords) {
  var sentSpanCoord = [], sentencePolygonCoordinates = [];
  var newText =  "";
  var oldText = $(textElementID).text().trim();
  newText = oldText
  var sortFunc = function(a,b) { return a.start - b.start; };
  startEndCoords.sort(sortFunc)
  var spanCharAcc = 0
  //put a span for each sentence
  for (var i = 0, len = startEndCoords.length; i < len; i++) {
    start = startEndCoords[i]['start'];
    end = startEndCoords[i]['end'];
    // for correct string slicing
    if (start == 0) {
      start = 1;
    }
    newText = newText.slice(0, start - 1 + spanCharAcc) + '<span>' + newText.slice(start - 1 + spanCharAcc)
    spanCharAcc = spanCharAcc + 6
    newText = newText.slice(0, end - 1 + spanCharAcc) + '</span>' + newText.slice(end - 1 + spanCharAcc)
    spanCharAcc = spanCharAcc + 7
  }

  $(textElementID).html(newText);
  console.log(newText)
  $spans = $(textElementID).find('span');
  $spans.each(function(){
    var $span = $(this),
        $offset = $span.offset();
    $offset.width = $span.innerWidth();
    $offset.height = $span.innerHeight();
    $offset.sentence = $span.text();
    sentSpanCoord.push($offset);
  });
  $(textElementID).html(oldText); //get back to original text without spans
  console.log(sentSpanCoord)

// loop over each sentence of the paragraph
  for(var i=0; i<sentSpanCoord.length;i++){
    var paragraphText = oldText;
    var sentenceStartPosition = paragraphText.indexOf(sentSpanCoord[i].sentence);
    var sentenceEndPosition = paragraphText.indexOf(sentSpanCoord[i].sentence) + sentSpanCoord[i].sentence.length-1;
    var coordofSentStartPosition = coordinatesofChar[sentenceStartPosition];
    var coordofSentEndPosition = coordinatesofChar[sentenceEndPosition];

    // eight points needed to build the polygon
    sentencePolygonCoordinates.push(
      {sentence:sentSpanCoord[i].sentence, start:sentenceStartPosition, end: sentenceEndPosition,
      numofwords:sentSpanCoord[i].sentence.split(" ").length,
      polygonCoords:[
      {x:coordofSentStartPosition.left, y:coordofSentStartPosition.top},
      {x:coordofSentStartPosition.left, y:coordofSentStartPosition.top+coordofSentStartPosition.height},
      {x:sentSpanCoord[i].left, y:coordofSentStartPosition.top+coordofSentStartPosition.height},
      {x:sentSpanCoord[i].left, y:sentSpanCoord[i].top+ sentSpanCoord[i].height},
      {x:coordofSentEndPosition.left+coordofSentEndPosition.width, y:coordofSentEndPosition.top+coordofSentEndPosition.height},
      {x:coordofSentEndPosition.left+coordofSentEndPosition.width, y:coordofSentEndPosition.top},
      {x:sentSpanCoord[i].left + sentSpanCoord[i].width, y:coordofSentEndPosition.top},
      {x:sentSpanCoord[i].left + sentSpanCoord[i].width, y:sentSpanCoord[i].top}
    ]});
  }
  return sentencePolygonCoordinates;
};


//coordinates of each sentence with index, each word within sentence with index, num of word in each sentence
function aggregateDataIntoJSON(charData, sentenceData, wordData){
  var aggregatedData = {charData:charData, sentenceData:sentenceData, wordData:wordData};
  return aggregatedData;
}

//function to sav coordinates
function sendJSONtoTornado(jsonObj, MMDid){
  jsonObj.filename = MMDid+'.json';
  $.ajax({
    url: '/saveCoordinates',

    data: JSON.stringify(jsonObj),
    dataType: "JSON",
    type: "POST",
    success: function ( data , status_text, jqXHR) {
      console.log('ajax success')
    },
    error: function ( data , status_text, jqXHR ) {
      console.log('ajax fail')
    },
  });

}

//check whether a point is within the polygon vs
function inside(point, vs) {
  // ray-casting algorithm based on
  // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

  var x = point[0], y = point[1];
  //console.log(x+','+y);
  var inside = false;
  for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {

    var xi = vs[i][0], yi = vs[i][1];
    var xj = vs[j][0], yj = vs[j][1];

    //console.log(xi,yi);
    //console.log(xj,yj);

    var intersect = ((yi > y) != (yj > y))
        && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }

  return inside;
};

//assumption is that word would not be in multiple lines
function findCoordinatesofWords(textElementID,coordinatesofChar) {
  var oldText = $(textElementID).text().trim();
  var words = oldText.split(" ");
  var wordCoordintes = [];
  //for the first word
  wordCoordintes.push({word:words[0], start:0, end:words[0].length,
    coords:[{x:coordinatesofChar[0].left,y:coordinatesofChar[0].top},
      {x:coordinatesofChar[words[0].length-1].left+coordinatesofChar[words[0].length-1].width,
       y:coordinatesofChar[words[0].length-1].top+coordinatesofChar[words[0].length-1].height}]});


  //for the remaining words
  for(var i=1;i<words.length;i++){
    var startPos = words.slice(0,i).join(" ").length; //get the length of all previous characters
     wordCoordintes.push({word:words[i], start:startPos, end:startPos + words[i].length,
      coords:[{x:coordinatesofChar[startPos].left,y:coordinatesofChar[startPos].top},
        {x:coordinatesofChar[words[i].length-1].left+coordinatesofChar[words[i].length-1].width,
         y:coordinatesofChar[words[i].length-1].top+coordinatesofChar[words[i].length-1].height}]});
  }
  return wordCoordintes;

}
