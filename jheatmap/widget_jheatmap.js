function getJHeatmapWidgetInstance(WidgetManager) {
    loadCSS();

    // Define the D3ForceDirectedGraphView
    var jHeatmapWidget = IPython.DOMWidgetView.extend({

		render: function(){

		    this.guid = 'jheatmap' + IPython.utils.uuid();
		    this.model.on('msg:custom', this.on_msg, this);
		    this.has_drawn = false;
            this.$el.text("Hello jHeatmap!");
            this.setElement($('<div/>', {id: this.guid, style: "width:100%"}));

		},

		on_msg: function(message){

		    if (this.lastmessage == message) {
		        // for some reason, the messages arrive twice
		        return;
		    }
		    this.lastmessage = message;


		    //console.log("message received! : " + JSON.stringify(message));

		    var action = message.action;
		    var value = message.value.replace("GUID", this.guid);

		    if (action=='draw') {
		        this._inputData = value
                this.update();
		    } if (action=='exec') {
	            var heatmap = $("#" + this.guid)[0]._heatmapInstance;
	            value.split(";").forEach(function(value){
	                cmd = value.trim();
	                if (cmd.length < 2 || cmd.substring(0,7) != "heatmap") {
	                    return;
	                }
	                console.log("executing: " + cmd)
                    eval("(" + cmd + ")");
	            });
                heatmap.drawer.paint();
		    }
		},

		update: function(){
		    if (this._inputData == undefined) {
                         console.log("bad update!");
                         return;
            }
		    if (!this.has_drawn) {
			    this.has_drawn = true;
			    //var width = this.model.get('width'),
			    //var height = this.model.get('height');
                //this._inputData = eval("({data : { values : new jheatmap.readers.TableHeatmapReader( { url : 'data/genomic-alterations.tsv'} ) }})");

                var drawdiv = $("#" + this.guid);
                var options = eval("( " + this._inputData  + ")");
                drawdiv.heatmap(options);
		    }
		    return jHeatmapWidget.__super__.update.apply(this);
		},
	});

	return jHeatmapWidget;
}

function loadCSS() {
	var $ = document; // shortcut
	var cssId = 'myCss';  // you could encode the css path itself to generate id..
	if (!$.getElementById(cssId))
	{
	    var head  = $.getElementsByTagName('head')[0];
	    var link  = $.createElement('link');
	    link.id   = cssId;
	    link.rel  = 'stylesheet';
	    link.type = 'text/css';
	    link.href = 'jheatmap/dependencies/jheatmap/css/jheatmap-1.0.0.css';
	    link.media = 'all';
	    head.appendChild(link);
	}
}

