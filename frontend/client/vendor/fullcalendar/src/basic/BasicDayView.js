
fcViews.basicDay = BasicDayView;

function BasicDayView(element, calendar) { // TODO: make a DayView mixin
	var t = this;
	
	
	// exports
	t.incrementDate = incrementDate;
	t.render = render;
	
	
	// imports
	BasicView.call(t, element, calendar, 'basicDay');


	function incrementDate(date, delta) {
		var out = date.clone().stripTime().add(delta, 'days');
		out = t.skipHiddenDays(out, delta < 0 ? -1 : 1);
		return out;
	}


	function render(date) {

		t.start = t.intervalStart = date.clone().stripTime();
		t.end = t.intervalEnd = t.start.clone().add(1, 'days');

		t.title = calendar.formatDate(t.start, t.opt('titleFormat'));

		t.renderBasic(1, 1, false);
	}
	
	
}
