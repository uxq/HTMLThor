var testFiles;

htmlthorApp.controller('ResultsController', function ($scope, resultsService) {

    //console.log("Results Controller loaded.");

    //console.log(resultsService.getResults());
	
	$scope.loadedEverything = false;
	
	$scope.currentResults = resultsService.getResults();

	$scope.totalSyntax = 0;
	$scope.totalSemantic = 0;
	$scope.totalDeprecated = 0;
	$scope.totalPractice = 0;
	$scope.totalErrors = 0;

	$scope.totalSyntaxTotalCount = 0;
	$scope.totalSemanticTotalCount = 0;
	$scope.totalDeprecatedTotalCount = 0;
	$scope.totalPracticeTotalCount = 0;
	
	$scope.activeFile = 0;
	
	$scope.areMultipleFiles = false;

	$scope.isZipFile = true; // return to false once design is finished

	//tempt
	$scope.zipResults = getZipResults();
	generateZipDisplay($scope.zipResults);

	// add class for when results exist on the site.
	$("body").addClass("state-resultsExist");	
	
	$scope.multipleFiles = [];	
	
	$scope.calculateTotalErrorCounts = function() {
	
		for (var i = 0; i < $scope.multipleFiles.length; i++) {
		
			
		
		}
		
	}
	
	$scope.isThisActiveFile = function(numberToCheck) {
	
		//console.log("Active file is:", $scope.activeFile);
		if (numberToCheck == $scope.activeFile) return true;
		else return false;
	
	}
	
	$scope.setActiveFile = function(numberToSet) {
	
		//console.log("Set active file!!!", numberToSet);
	
		$scope.activeFile = numberToSet;
		$scope.currentResults = $scope.multipleFiles[numberToSet];
	
	}
	
	// It doesn't belong here, but I'm gonna take care of some of the data...
	
	$scope.escapeHtml = function(htmlToEscape) {
		var htmlElements = [["<","&lt;"],[">","&gt;"],["\"","&quot;"],["\'","&#39;"]];
		for(var j=0; j<htmlElements.length; j++) {
			reg = new RegExp(htmlElements[j][0], "gi");
			htmlToEscape = htmlToEscape.replace(reg,htmlElements[j][1]);
		}
		return htmlToEscape;
	}
	
	$scope.sanitizeSource = function() {
	
		//console.log("Before sanitization", $scope.multipleFiles);
		
		for (var j = 0; j < $scope.multipleFiles.length; j++) {
			var sourceCodeLength = $scope.multipleFiles[j].sourceCode.length;
		
			for (var i = 0; i < sourceCodeLength; i++) {
				$scope.multipleFiles[j].sourceCode[i] = $scope.escapeHtml($scope.multipleFiles[j].sourceCode[i]);
			}
			
		}
			
		//console.log("After sanitization", $scope.multipleFiles);
		
		generateSourceSection($scope.multipleFiles);
		
	}
	
	$scope.getStoredResults = function() {
		$scope.multipleFiles = resultsService.getResults();
	
		if($scope.multipleFiles.length > 1) {
		
			$scope.areMultipleFiles = true;
		
		}

		//$scope.multipleFiles = $scope.oldFiles; // !!! REMOVE THIS !!!
	}
	
	$scope.prepCounts = function() {

		testFiles = $scope.multipleFiles;
		
		for(var i = 0; i < $scope.multipleFiles.length ; i++) {
			// console.log("i is: " + i, "0 obj is: ", $scope.multipleFiles[0]);
			// console.log("Checking this file for lengths:", $scope.multipleFiles[i], $scope.multipleFiles[i].syntaxErrors);
			if(!$scope.multipleFiles[i].fileName) {
				$scope.multipleFiles[i] = $scope.multipleFiles[i][0];
			}

			var syntaxTotalCount = 0;
			var semanticTotalCount = 0;
			var deprecatedTotalCount = 0;
			var practiceTotalCount = 0;

			syntaxTotalCount += $scope.multipleFiles[i].syntaxErrors.length;
			$scope.multipleFiles[i].syntaxCount = syntaxTotalCount;
			semanticTotalCount += $scope.multipleFiles[i].semanticErrors.length;
			$scope.multipleFiles[i].semanticCount = semanticTotalCount;
			deprecatedTotalCount += $scope.multipleFiles[i].deprecatedErrors.length;
			$scope.multipleFiles[i].deprecatedCount = deprecatedTotalCount;
			practiceTotalCount += $scope.multipleFiles[i].practiceErrors.length;
			$scope.multipleFiles[i].practiceCount = practiceTotalCount;
		
			$scope.totalSyntax += syntaxTotalCount;
			$scope.totalSemantic += semanticTotalCount;
			$scope.totalDeprecated += deprecatedTotalCount;
			$scope.totalPractice += practiceTotalCount;
			
		}
		
		$scope.totalErrors = $scope.totalSyntax + $scope.totalSemantic + 
			$scope.totalDeprecated + $scope.totalPractice;
		
	}
	
	$scope.getStoredResults();
	$scope.prepCounts();
	$scope.setActiveFile(0); // important
	$scope.sanitizeSource();
	initHelpExplanation();
	// $scope.calculateTotalErrorCounts();

});

function escapeHtml(htmlToEscape) {
	var htmlElements = [["<","&lt;"],[">","&gt;"],["\"","&quot;"],["\'","&#39;"]];
	for(var j=0; j<htmlElements.length; j++) {
		reg = new RegExp(htmlElements[j][0], "gi");
		htmlToEscape = htmlToEscape.replace(reg,htmlElements[j][1]);
	}
	return htmlToEscape;
}

function unescapeHtml(htmlToUnescape) {
		var htmlElements = [["<","&lt;"],[">","&gt;"],["\"","&quot;"],["\'","&#39;"]];
		for(var j=0; j<htmlElements.length; j++) {
			reg = new RegExp(htmlElements[j][1], "gi");
			if (htmlToUnescape)
			htmlToUnescape = htmlToUnescape.replace(reg,htmlElements[j][0]);
		}
		return htmlToUnescape;
}

function generateSourceSection(sourceFiles) {
	//console.log("Aww yeah buddy, I'm populating the source code section!", sourceFiles);
	var sourceCodeContainer = $("#sourceCodeContainer");
	var listContainer = $("#template--sourceCode").find(".template");
	var listItem = $("#template--sourceCode-line").find(".template");
	
	var sourceErrors = sourceFiles;
	var sourceErrorsCalculated = handleSourceErrors(sourceFiles);
	
	var templateLineError = $("#template--sourceCode-lineError").find(".template");
	var templateLineErrorInfo = $("#template--sourceCode-info").find(".template");
	
	for(var i = 0; i < sourceErrors.length; i++) {
	
		var htmlListContainer = listContainer.clone();
		
		var sourceCode = sourceErrors[i].sourceCode;
		var sourceCodeLength = sourceCode.length;	
		// console.log("Checking file number: " + i, sourceCode);
		
		for(var j = 0; j < sourceCodeLength; j++) {
			var htmlListItem = listItem.clone();
			// console.log("Source: " + sourceCode[j]);
			
			htmlListItem.find(".sourceCode-number").html(j + 1);
			htmlListItem.find(".sourceCode-code pre").html(sourceCode[j]);
			
			htmlListContainer.append(htmlListItem);
			
		}
		
		for(var j = 0; j < sourceErrorsCalculated[i].length; j++) {
			// console.log("@#@ Errors: ", sourceErrorsCalculated[i][j]);
			var thisLine = sourceErrorsCalculated[i][j].line;
			var thisIndex = thisLine - 1;
			var htmlThisLine = htmlListContainer.find("li:eq(" + thisIndex + ")");
			htmlThisLine.addClass("hasErrors");
			htmlThisLine.find(".sourceCodeErrorCount").html(sourceErrorsCalculated[i][j].errors.length);
			
			for(var k = 0; k < sourceErrorsCalculated[i][j].errors.length; k++) {
				var htmlLineError = templateLineError.clone();
				var htmlErrorInfo = templateLineErrorInfo.clone();
				htmlLineError.find(".sourceCode-lineError").html(sourceErrorsCalculated[i][j].errors[k].error);
				
				htmlErrorInfo.find(".sourceCodeErrorInfo-excerpt").html(sourceErrorsCalculated[i][j].errors[k].excerpt);
				htmlErrorInfo.find(".sourceCodeErrorInfo-msg").html(escapeHtml(sourceErrorsCalculated[i][j].errors[k].message));
				htmlErrorInfo.find(".sourceCodeErrorInfo-colStart").html(sourceErrorsCalculated[i][j].errors[k].column);
				htmlErrorInfo.find(".sourceCodeErrorInfo-colEnd").html(sourceErrorsCalculated[i][j].errors[k].end);
				
				var errorType = sourceErrorsCalculated[i][j].errors[k].type;
				var htmlErrorType = htmlErrorInfo.find(".errorType");
				
				switch(errorType) {
					case "syntax":
						htmlErrorType.addClass("errorType--syntax");
						htmlErrorType.html("Syntax");
						break;
					case "semantic":
						htmlErrorType.addClass("errorType--semantic");
						htmlErrorType.html("Semantic");
						break;
					case "deprecated":
						htmlErrorType.addClass("errorType--deprecated");
						htmlErrorType.html("Deprecated");
						break;
					case "practice":
						htmlErrorType.addClass("errorType--practice");
						htmlErrorType.html("Best Practice");
						break;
				}				
				
				htmlThisLine.find(".sourceCode-code-errorsCont").append(htmlLineError);
				htmlThisLine.find(".sourceCodeErrorInfo").append(htmlErrorInfo);
			}
			
		}
		
		// go into sourceErrorsCalculated
		// loop through each errors block
		// find the li for that line
		// add in extra stuff
		
		
		sourceCodeContainer.append(htmlListContainer);
		
	}

	// TODO: Need this to init scrollbar
	//initSourceScrollbar();
	
}

function handleSourceErrors(sourceFiles) {
	var sourceErrors = sourceFiles;
	var sourceWithErrors = [];
	
	for(var i = 0; i < sourceFiles.length; i++) {
		var thisFilesErrors = [];
		var errorsWithHighlights = [];
		
		thisFilesErrors = thisFilesErrors.concat(sourceFiles[i].syntaxErrors);
		thisFilesErrors = thisFilesErrors.concat(sourceFiles[i].semanticErrors);
		thisFilesErrors = thisFilesErrors.concat(sourceFiles[i].deprecatedErrors);
		thisFilesErrors = thisFilesErrors.concat(sourceFiles[i].practiceErrors);
		
		// console.log("The errors for this line!!!", thisFilesErrors);
		
		// var queryResult = Enumerable.From(thisFilesErrors)
		// .Where(function (x) { return x.line == 6 }).Select(function (x) { retun x.line });
		
		var queryResult = Enumerable.From(thisFilesErrors)
		.GroupBy(function (x) { return x.line })
		.ToArray();
		
		for(var j = 0; j < queryResult.length; j++) {
			var lineNumber = queryResult[j].source[0].line;
			var originalSourceLine = sourceFiles[i].sourceCode[lineNumber - 1];
			var newSourceLine = unescapeHtml(originalSourceLine);
			
			var linesErrorDetails = {};
			linesErrorDetails.line = lineNumber;
			linesErrorDetails.errors = [];
			
			// console.log("For each error in queryresult: ", queryResult[j].source);
			
			// gonna need to convert the escaped html back...
			
			// need to track offset when adding stuff...
			// add <span> stuff before start
			// get length of <span> stuff and add after end + length
			// now for the next error, need the offset...
			
			for(var q = 0; q < queryResult[j].source.length; q++) {
				// console.log("This error!!!");
				var startCol = queryResult[j].source[q].column - 1;
				var endCol = queryResult[j].source[q].end - 1;
				
				//console.log("%%DEBUGGING: Start: " + startCol + " End: " + endCol);
				
				var startString = newSourceLine ? newSourceLine.substring(0, startCol) : '';
				var middleString = newSourceLine ? newSourceLine.substring(startCol, endCol) : '';
				var endString = newSourceLine ? newSourceLine.substring(endCol) : '';
				
				var beginningSpan = "<span class='errorType--" + queryResult[j].source[q].type +"'>";
				var endSpan = "</span>"
				
				startString = escapeHtml(startString);
				middleString = escapeHtml(middleString);
				endString = escapeHtml(endString);
				
				var finalError = startString + beginningSpan + middleString + endSpan + endString;
				
				var errorObj = {};
				errorObj.error = finalError;
				errorObj.message = queryResult[j].source[q].message;
				errorObj.column = queryResult[j].source[q].column;
				errorObj.end = queryResult[j].source[q].end;
				errorObj.type = queryResult[j].source[q].type;
				errorObj.excerpt = middleString;
				
				// grab everything in the string before the start
				// grab everything in the string after the end
				
				// console.log("There's an error with the excerpt of: " + excerpt);
				
				linesErrorDetails.errors.push(errorObj);
				
				//var excerpt = get string from thingy...
			}
			
			errorsWithHighlights.push(linesErrorDetails);
			
			// console.log("Errors at line: " + lineNumber, "Line contains: " + sourceFiles[i].sourceCode[lineNumber - 1]);
			// console.log("All of the errors for this line: " + queryResult[j].source[0].line, queryResult[j].source);
		}
		
		sourceWithErrors.push(errorsWithHighlights);
		//console.log("Full errors with their codes: ", errorsWithHighlights);
		
		
	}
	
	//console.log("I'm handling the source errors!", sourceWithErrors);
	
	return sourceWithErrors;
}

function initHelpExplanation() {
	console.log("Initiated help section");

	$(".resultPreview-help").click(function() {
		$("#explanationSection").slideDown();
	});
	
	$("#explanation-close").click(function() {
		$("#explanationSection").slideUp();
	});

}



/*
 *
 *	Scrollbar...

	When the user scrolls, change from

 *
 */

// Code from: http://stackoverflow.com/a/9617517


function initSourceScrollbar() {

	var scrollTimer, lastScrollFireTime = 0;

	initScrollingAbility();

	$(window).on('scroll', function() {

	    var minScrollTime = 100;
	    var now = new Date().getTime();

	    function processScroll() {
	        var sourceContainer = $("#sourceCodeContainer");
	        if(isScrolledIntoView(sourceContainer)) {
	        	$("body").addClass("state-sourceOnScreen");
	        } else {
	        	$("body").removeClass("state-sourceOnScreen");
	        }
	    }

	    if (!scrollTimer) {
	        if (now - lastScrollFireTime > (3 * minScrollTime)) {
	            processScroll();   // fire immediately on first scroll
	            lastScrollFireTime = now;
	        }
	        scrollTimer = setTimeout(function() {
	            scrollTimer = null;
	            lastScrollFireTime = new Date().getTime();
	            processScroll();
	        }, minScrollTime);
	    }
	});

}

// Code from: http://stackoverflow.com/a/488073 
function isScrolledIntoView(elem)
{
    var $elem = $(elem);
    var $window = $(window);

    var docViewTop = $window.scrollTop();
    var docViewBottom = docViewTop + $window.height();

    var elemTop = $elem.offset().top;
    var elemBottom = elemTop + $elem.height();

    return (((elemBottom + 60) <= docViewBottom));
}

// draggable slider

function initScrollingAbility() {

	calculateScrollingProperties();

	var knob = $("#scrollKnob");
	var bar = $("#scrollBar");

	var heldDown = false;

	knob.mousedown(function(e){
		heldDown = true;
		
	});

	$("body").mouseup(function(){
		heldDown = false;
	});

	$("body").mousemove(function(e) {
		if(heldDown) {
			var knobWidth = knob.width();
			var barWidth = bar.width();
			newPosition = e.pageX;
			leftOffset = bar.offset().left;
			finalPosition = newPosition - leftOffset;
			if(finalPosition > (barWidth - knobWidth)) {
				finalPosition = barWidth - knobWidth;
			}
			knob.css("left", finalPosition);
		}
	});

	// $("#scrollKnob").draggable({
	// 	axis : "x"
	// 	// drag: function() {
	// 	// 	var offset = $(this).offset();
	// 	// 	var xPos = offset.left;
	// 	// }
	// });

}

function calculateScrollingProperties() {

	var sourceCodeContainer = $("#sourceCodeContainer");
	var resultsSourceSection = $("#resultsSourceSection");

	var originalWidth = sourceCodeContainer.width();

	resultsSourceSection.css("position", "absolute");

	var fullWidth = sourceCodeContainer.width();

	resultsSourceSection.css("position", "relative");

	if(fullWidth > originalWidth) {
		setScrollingProperties(fullWidth, originalWidth);
		$("body").addClass("needSourceScroll");
	} else {
		$("body").removeClass("needSourceScroll");
	}

}

function setScrollingProperties(fullWidth, originalWidth) {

	var knob = $("#scrollKnob");
	var bar = $("#scrollBar");

	var knobWidth = originalWidth / fullWidth * 100;

	knob.css("width", knobWidth + "%");

	console.log("Set bar width to " + knobWidth + "%");

}

// temp

function getZipResults() {
	var tempZip = {
		"structure" : [
			{
				"name" : "index.html",
				"extension" : "html",
				"type" : "file",
				"children" : [],
				"broken" : true,
				"brokenCount" : 4,
				"locationBad" : false,
			},
			{
				"name" : "about.html",
				"extension" : "html",
				"type" : "file",
				"children" : [],
				"broken" : false,
				"brokenCount" : 0,
				"locationBad" : false,
			},
			{
				"name" : "style.css",
				"extension" : "css",
				"type" : "file",
				"children" : [],
				"broken" : false,
				"brokenCount" : 0,
				"locationBad" : true,
			},
			{
				"name" : "cool.jpg",
				"extension" : "jpg",
				"type" : "file",
				"children" : [],
				"broken" : false,
				"brokenCount" : 0,
				"locationBad" : true,
			},
			{
				"name" : "images",
				"extension" : "",
				"type" : "folder",
				"children" : [
					{
						"name" : "groovy.jpg",
						"extension" : "jpg",
						"type" : "file",
						"children" : [],
						"broken" : false,
						"brokenCount" : 0,
						"locationBad" : false,
					},
					{
						"name" : "bg.jpg",
						"extension" : "jpg",
						"type" : "file",
						"children" : [],
						"broken" : false,
						"brokenCount" : 0,
						"locationBad" : false,
					}
				],
				"broken" : false,
				"brokenCount" : 0,
				"locationBad" : false,
			},
			{
				"name" : "css",
				"extension" : "",
				"type" : "folder",
				"children" : [
					{
						"name" : "home.css",
						"extension" : "css",
						"type" : "file",
						"children" : [],
						"broken" : false,
						"brokenCount" : 0,
						"locationBad" : false,
					},
					{
						"name" : "about.css",
						"extension" : "css",
						"type" : "file",
						"children" : [],
						"broken" : false,
						"brokenCount" : 0,
						"locationBad" : false,
					},
					{
						"name" : "plugins",
						"extension" : "",
						"type" : "folder",
						"children" : [
							{
								"name" : "random.css",
								"extension" : "css",
								"type" : "file",
								"children" : [],
								"broken" : false,
								"brokenCount" : 0,
								"locationBad" : false,
							},
							{
								"name" : "anotherFolder",
								"extension" : "",
								"type" : "folder",
								"children" : [
									{
										"name" : "deeper",
										"extension" : "",
										"type" : "folder",
										"children" : [
											{
												"name" : "randomFile.doc",
												"extension" : "doc",
												"type" : "file",
												"children" : [],
												"broken" : false,
												"brokenCount" : 0,
												"locationBad" : false,
											}
										],
										"broken" : false,
										"brokenCount" : 0,
										"locationBad" : false,
									},
								],
								"broken" : false,
								"brokenCount" : 0,
								"locationBad" : false,
							},
						],
						"broken" : false,
						"brokenCount" : 0,
						"locationBad" : false,
					},
				],
				"broken" : false,
				"brokenCount" : 0,
				"locationBad" : false,
			},
		]
	};

	return tempZip;
}

function generateZipDisplay(zipData) {

	var zipList = $("#zipList");

	for(var i = 0; i < zipData.structure.length; i++) {
		var zipItem = generateZipDisplayItem(zipData.structure[i]);
		zipList.append(zipItem);
	}

}

function generateZipDisplayItem(zipItemData, childLevel) {

	var zipItem = $("#template--zip-item").find(".template").clone();

	if(!childLevel) {
		var childLevel = 0;
	}

	if(isOdd(childLevel)) {
		zipItem.addClass("lightShade");
	} else {
		zipItem.addClass("darkShade");
	}

	zipItem.find(".zipItemName").html(zipItemData.name);

	if(zipItemData.broken) {
		zipItem.find(".zipItem").addClass("error");
		zipItem.find(".brokenCount").html(zipItemData.brokenCount);
	}

	if(zipItemData.locationBad) {
		zipItem.find(".zipItem").addClass("warning");
		switch(zipItemData.extension) {case "html":
			case "css":
				zipItem.find(".locationSuggestion").html("css/");
				break;
			case "js":
				zipItem.find(".locationSuggestion").html("js/");
				break;
			case "jpg":
			case "png":
			case "gif":
			case "jpeg":
			case "bmp":
				zipItem.find(".anOrA").html("n");
				zipItem.find(".locationSuggestion").html("images/");
				break;
			default:
				zipItem.find(".anOrA").html("n");
				zipItem.find(".locationSuggestion").html("unknown???/");
				break;
		}
	}

	if(zipItemData.type == "folder") {
		zipItem.find(".zipItem").addClass("folder");
		zipItem.addClass("folder");
		zipItem.find(".zipItemIcon").addClass("icon-folder-open-empty");
		if(zipItemData.children.length == 0) {
			zipItem.find(".zipItem").addClass("emptyFolder");
		}
	} else {

		switch(zipItemData.extension) {
			case "html":
			case "css":
			case "js":
			case "php":
				zipItem.find(".zipItemIcon").addClass("icon-file-code");
				break;
			case "jpg":
			case "png":
			case "gif":
			case "jpeg":
			case "bmp":
				zipItem.find(".zipItemIcon").addClass("icon-file-image");
				break;
			default:
				zipItem.find(".zipItemIcon").addClass("icon-doc");
				break;
		}

	}

	if(zipItemData.children.length > 0) {
		var zipItemChildren = zipItem.find(".zipItemChildren");
		for(var i = 0; i < zipItemData.children.length; i++) {
			var newZipItem = generateZipDisplayItem(zipItemData.children[i], (childLevel + 1));
			zipItemChildren.append(newZipItem);
		}
	}

	return zipItem;

}

function isOdd(num) {
	return (num % 2) == 1;
}