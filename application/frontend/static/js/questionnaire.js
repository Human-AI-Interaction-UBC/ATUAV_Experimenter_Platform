
/**
 * Demo in action!
 */

    // SHOP ELEMENT
var shop = document.querySelector('#star_rating');
var questionList = document.querySelector('#questionList');

console.log(questionObj);


var questionArray = [];

for(var i=0;i<questionObj.length;i++){
  var questionData = {
    mmdId: questionObj[i][0],
    qid: questionObj[i][1],
    questionBody: questionObj[i][2],
    responseType: questionObj[i][3],
    answers: questionObj[i][4],
    correctAnswer: questionObj[i][6],
    rating: null
  };
  console.log(questionData);

  questionArray.push(questionData);

  if(questionData.responseType==='Likert'){

      addRatingWidget(buildShopItem(questionData), questionData);
  }
  else if(questionData.responseType==='MC' || questionData.responseType==='TF'){
    $( "#questionList" ).append( buildMultipleChoiceQuestion(questionData));
  }
}

// // INITIALIZE
// (function init() {
//     for (var i = 0; i < starData.length; i++) {
//         addRatingWidget(buildShopItem(starData[i]), starData[i]);
//     }
// })();

 function buildMultipleChoiceQuestion(questionData){
   var  questionID = questionData.qid;

   var answers = questionData.answers.split(',');

    console.log(answers);

    var html = '<li id="li_'+questionID+'" >'+
      '<label class="description" id="label_'+questionData.qid + '" for="element_2">'+questionData.qid+'. '+questionData.questionBody+'</label>'+
      '<span>';

   for(var i=0;i<answers.length;i++){
     var answerOnly = answers[i].substring(4, i===answers.length-1?answers[i].length-2: answers[i].length-1);


     html+= '<input id="element_'+questionID+'_'+(i+1)+'" name="element_'+questionID+'" class="element radio" type="radio" value="'+answers[i].substring(2,3)+'" />'+
     '<label class="choice" >' +answerOnly+'</label>';
   }



      //'<input id="element_'+questionID+'_2" name="element_1" class="element radio" type="radio" value="2" />'+
      //'<label class="choice" for="element_2_2">False</label>'+
   html+='</span>'+
      '</li>';
    return html;
}
// BUILD SHOP ITEM
function buildShopItem(data) {
    var shopItem = document.createElement('div');

    var html = '<div class="c-shop-item__img"></div>' +
        '<div class="c-shop-item__details">' +
        // '<h3 class="c-shop-item__title">' + data.title + '</h3>' +
        '<table><tr><td width="340px"><p id="label_'+questionArray[i].qid+'" class="c-shop-item__questionBody"><b>'+questionArray[i].qid+'. ' + data.questionBody + '</b></p></td>' +
        '<td><ul class="c-rating"></ul></td></tr></table>' +
        '</div>';

    shopItem.classList.add('c-shop-item');
    shopItem.innerHTML = html;
    shop.appendChild(shopItem);

    return shopItem;
}

// ADD RATING WIDGET
function addRatingWidget(shopItem, data) {
    var ratingElement = shopItem.querySelector('.c-rating');
    var currentRating = data.rating;
    var maxRating = 5;
    var callback = function(rating) { //alert(rating);
        //console.log(data.id+","+rating+", "+data.rating)
        for (i=0;i,questionArray.length;i++){
            if(questionArray[i].qid==data.qid) {
              questionArray[i].rating=rating;
                break;
            }
        }
        console.log(questionArray);
    };
    var r = rating(ratingElement, currentRating, maxRating, callback);
}

function getSelectedValue(element){
    var txt="";
    for (i = 0; i < element.length; i++) {
        if (element[i].checked) {
            txt = txt + element[i].value + " ";
        }
    }
    return txt;

}

$( "form" ).submit(function( event ) {
  console.log('form');
   var answerList=[];
  var i, isCorrect = "";
  var questionUnanswered = false;
  for (i=0;i<questionArray.length;i++) {
    var answer = null;
    //console.log(questionArray[i]);
    if(questionArray[i].responseType==='Likert'){
      console.log(questionArray[i].rating);
      answer = questionArray[i].rating;
    }
    else if(questionArray[i].responseType==='MC' || questionArray[i].responseType==='TF'){
      //console.log(getSelectedValue("element_"+ questionArray[i].qid));
        console.log(questionArray[i]);
      console.log($('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val());
      answer = $('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val();
      if(questionArray[i].responseType==='TF'){
        isCorrect = $('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val() ==='T'? "Correct": "Incorrect";
      }
      else if(questionArray[i].responseType==='MC'){
        isCorrect = questionArray[i].correcAnswer===$('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val()? "Correct": "Incorrect";
      }

    }
    //console.log(questionArray[i].qid);
    //$("#li_"+questionArray[i].qid).css("color","red");
    if( answer===null | answer===undefined){
      console.log(questionArray[i].qid);
      $("#label_"+questionArray[i].qid).css("color","red");
      questionUnanswered =true;
      //break;
    }
    else{
      //answerList.push( {question:questionArray[i].qid, answer: answer});
      answerList.push( [answer,isCorrect]);
      $("#label_"+questionArray[i].qid).css("color","black");
    }
    isCorrect ="";
  }

  if(!questionUnanswered){
    $("#ErrorContainer").html("");
    $('#answers').val(JSON.stringify(answerList));

    return;
  }

  $("#ErrorContainer").html("<font color='red'>Please answers all the questions </font>");

//  $( "span" ).text( "Not valid!" ).show().fadeOut( 1000 );
  event.preventDefault();
});

/*
function submitPostStudy() {
    var f = document.forms[0];
    var txt="";
    var i;
    var questionUnanswered = false;
    for (i=0;i<questionArray.length;i++) {
      var answer = null;
      //console.log(questionArray[i]);
      if(questionArray[i].responseType==='Likert'){
        console.log(questionArray[i].rating);
        answer = questionArray[i].rating;
      }
      else if(questionArray[i].responseType==='MC' || questionArray[i].responseType==='TF'){
        //console.log(getSelectedValue("element_"+ questionArray[i].qid));
        console.log($('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val());
        answer = $('input[name='+"element_"+ questionArray[i].qid+']:checked', '#form_questionnaire').val();
      }
      //console.log(questionArray[i].qid);
      //$("#li_"+questionArray[i].qid).css("color","red");
      if( answer===null | answer===undefined){
        console.log(questionArray[i].qid);
        $("#label_"+questionArray[i].qid).css("color","red");
        questionUnanswered =true;
        //break;
      }
      else{
        $("#label_"+questionArray[i].qid).css("color","black");
      }

    }
    if(questionUnanswered){
      $("#ErrorContainer").html("<font color='red'>Please answers all the questions </font>");
    }
    else{
      $("#ErrorContainer").html("");
    }

    //console.log(starData);
/!*    console.log(f.element_1);
    for (i=0;i<starData.length;i++){
      //console.log(starData[i].rating);
      userstring+=starData[i].rating+",";
    }
    if(getSelectedValue(f.element_1)!=''){

      getSelectedValue();
      //userstring+=
      //    getSelectedValue(f.element_1)+","+$('#element_6').val()+","+$('#element_7').val();
      //console.log(userstring);

    }
    else {
        $('#li_1 .questionBody').css("color","red");
    }*!/
}*/
