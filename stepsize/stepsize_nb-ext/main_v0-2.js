define(['base/js/namespace', 'base/js/dialog', 'base/js/events', 'components/codemirror/lib/codemirror', 'jquery'], function(IPython, dialog, events, CodeMirror, $){

	var search = {
		help: 'Submits your search to Stepsize',
		icon : 'fa-search',
		help_index : '',
		handler : function (env) {
			var cell = env.notebook.get_selected_cell();
			if (cell.cell_type === "code") {
				var code = $(cell.input).find($('.CodeMirror'))[0].CodeMirror;
				var selected = code.getSelection();
				if (selected.length > 0) {
					getSearchResults(selected, cell);
				} else {
					var line = code.getLine(code.getCursor(true).line).trim();
					getSearchResults(line, cell);
				}
			}
		}
	};

	function getSelectionText() {
		console.log(uuid);
	    var text = "";
	    if (window.getSelection) {
	        text = window.getSelection().toString();
	    } else if (document.selection && document.selection.type != "Control") {
	        text = document.selection.createRange().text;
	    }
	    return text;
	}

	function getSearchResults(query, cell) {
		var url_base = "http://search.stepsize.com/api/v0.1/process-summary-query/?q=";
		var query_argument = query.trim().replace(' ', '|');
		var id_argument = "&uid=" + uid;
		var origin_argument = "&ori=jupyter_v0.1";
		var url = url_base + query_argument + id_argument + origin_argument;
		$.getJSON(url, function(data) {
			createHTMLResult(query, data, cell);
		});
	}

	function createHTMLResult(query, data, cell) {
		var query_id = data.query_id;
		// Base elements
		var raw_code = $('<code>').html(data.code_snippet);
		var query_argument = "?q=" + query.trim().replace(' ', '+');
		var stepsize_url = "http://www.stepsize.com/" + query_argument;
		// Components of the result
		var result = $('<div>');

		var so_link = $('<a>', {href: data.code_snippet_url,
								target: "_blank"}).html(data.code_snippet_url);

		var google_link = $('<a>', {href: data.google_search_url,
									target: "_blank"}).html('Google Search Results - ' + query);

		var function_signature = $('<a>', {href: data.entity_url,
										   target: "_blank"}).append($('<code>').html(data.entity_signature));

		var title = $('<a>', {href: data.entity_url,
							  target: "_blank"}).html(data.entity_name);

		var code = $('<p>').append($('<pre>').append(raw_code));

		var stepsize = $('<p>').append($('<a>', {href: stepsize_url,
												 target: "_blank"}).html('Stepsize Search Results - ' + query));

		var extra = $('<p>').html(data.extra_field);
		// Building the result
		if (data.entity_signature === null) {
			result.append(title);
		} else {
			result.append(function_signature);
		}
		if (data.code_snippet !== null) {
			result.append(code).append(so_link);
		}
		result.append(stepsize);
		result.append(google_link);
		if (data.extra_field !== null) {
			result.append(extra);
		}
		var data_content = {"text/plain": "<IPython.core.display.HTML object>",
							"text/html": result.prop('outerHTML')};
		var new_output = {"output_type": "display_data",
						  "data": data_content, "metadata": {}};
		cell.output_area.clear_output();
		cell.output_area.append_output(new_output);
	}

	var uid;

	function getUID() {
		$.getJSON('/uid', function(data) {
			uid = data.uid;
		});
	}

	var load_ipython_extension = function() {
		console.info('Stepsize extension activated.');
		var action_name = IPython.keyboard_manager.actions.register(
			search,
			'search',
			'stepsize'
		);
		IPython.keyboard_manager.command_shortcuts.add_shortcut('Alt-/', action_name);
		IPython.keyboard_manager.edit_shortcuts.add_shortcut('Alt-/', action_name);
		IPython.toolbar.add_buttons_group(['stepsize.search']);
		getUID();
	};

	return {load_ipython_extension: load_ipython_extension };
});
