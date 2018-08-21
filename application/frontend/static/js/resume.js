/**
 * Created by enamul on 4/4/2017.
 */

var selectHtml = "";

for(var i=0;i<userList.length;i++){
  //console.log(userList[i]);
  selectHtml+= '<option value="'+userList[i]+'">'+userList[i]+'</option>';
}
console.log(selectHtml);
$("#userOptions").html(selectHtml);


/*
$( "form" ).submit(function( event ) {
  $("#userOptions").change(function() {
    currentuser = $(this).find("option:selected").text();
  });
  console.log(selectHtml);
  $("#userOptions").html(selectHtml);

  $( "form" ).submit(function( event ) {
    var f = document.forms[0];
    $('#selecteduser').val(currentuser);
    return;
  });
  event.preventDefault();
});*/
