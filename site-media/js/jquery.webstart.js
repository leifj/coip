/*
 * jQuery.webstart
 * 
 * Written by Leif Johansson (leifj@nordu.net)
 * 
 * Licensed under BSD
 * Requires http://java.com/js/deployJava.js
 */

String.prototype.startsWith = function(str) {return (this.match("^"+str)==str)}

jQuery.fn.webstart = function(options) {
	if (typeof(options.minVersion) == "undefined")
		options.minVersion = "1.6.0";
	
	this.each(function() {
		var jnlp = options.jnlp;
		if (!jnlp.startsWith("http")) {
			var dir = location.href.substring(0,location.href.lastIndexOf('/')+1);
	 	    jnlp = dir+jnlp
		}
		
		if (deployJava.returnPage == null) {
		       deployJava.returnPage = jnlp;
		}
		
		$(this).click(function() {
	    	if (!deployJava.isWebStartInstalled(options.minVersion)) {
	    	   if (deployJava.installLatestJRE()) {
	    	      if (deployJava.launch(jnlp)) {}
	    	   }
	    	} else {
	    	   if (deployJava.launch(jnlp)) {}
	    	}
	    });
	});
}