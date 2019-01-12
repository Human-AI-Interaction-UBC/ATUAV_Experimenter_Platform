var ReferenceDisplay = function() {
  return {
    restrict: 'E',
    replace: true,
    templateUrl: 'static/angular/referencedisplay.html',
    controller: ReferenceDisplayCtrl,
    scope: {
      ref: '=',
      onReferenceSelect: '&',
      text: '='
    }
  };
};
