
fcViews.month = MonthView;

function MonthView(element, calendar) {
	var t = this;
	
	
	// exports
	t.incrementDate = incrementDate;
	t.render = render;
	
	
	// imports
	BasicView.call(t, element, calendar, 'month');


	function incrementDate(date, delta) {
		return date.clone().stripTime().add(delta, 'months').startOf('month');
	}


	function render(date) {

		t.intervalStart = date.clone().stripTime().startOf('month');
		t.intervalEnd = t.intervalStart.clone().add(1, 'months');

		t.start = t.intervalStart.clone();
		t.start = t.skipHiddenDays(t.start); // move past the first week if no visible days
		t.start.startOf('week');
		t.start = t.skipHiddenDays(t.start); // move past the first invisible days of the week

		t.end = t.intervalEnd.clone();
		t.end = t.skipHiddenDays(t.end, -1, true); // move in from the last week if no visible days
		t.end.add((7 - t.end.weekday()) % 7, 'days'); // move to end of week if not already
		t.end = t.skipHiddenDays(t.end, -1, true); // move in from the last invisible days of the week

		var rowCnt = Math.ceil( // need to ceil in case there are hidden days
			t.end.diff(t.start, 'weeks', true) // returnfloat=true
		);
		if (t.opt('weekMode') == 'fixed') {
			t.end.add(6 - rowCnt, 'weeks');
			rowCnt = 6;
		}

		t.title = calendar.formatDate(t.intervalStart, t.opt('titleFormat'));

		t.renderBasic(rowCnt, t.getCellsPerWeek(), true);
	}
	
	
}
