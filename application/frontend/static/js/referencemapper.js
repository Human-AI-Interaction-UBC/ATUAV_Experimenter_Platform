!function() {
  var ReferenceMapper = function(visual_references) {
    var self = this;
    this.visual_references = visual_references;
    this.marks_to_tuples = this.visual_references.references.reduce(
      function(acc, val) {
        acc[val.mark_id] = val;
        return acc;
      }, {});
    this.tuples_to_marks = {};
    this.visual_references.references.forEach(
      function(reference) {
        reference.tuple_ids.forEach(function(tuple_id) {
          self.tuples_to_marks[tuple_id] = reference.mark_id;
        });
      });

  };
  ReferenceMapper.prototype = {
    constructor: ReferenceMapper,
    getReferringMarks: function(tuple_ids) {
      var self = this;
      return tuple_ids.map(function(tuple_id) {
        return self.tuples_to_marks[tuple_id];
      });
    },
    getReferentTuples: function(mark_ids) {
      var self = this;
      return mark_ids.map(function(mark_id) {
        return self.marks_to_tuples[mark_id];
      });
    }
  }

  window.ReferenceMapper = ReferenceMapper;
}()
