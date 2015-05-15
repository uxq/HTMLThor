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
	
	$scope.activeFile = 0;
	
	$scope.areMultipleFiles = false;

	// add class for when results exist on the site.
	$("body").addClass("state-resultsExist");	
	
	$scope.multipleFiles = [];	
	
	$scope.oldFiles = [
	
		{
			fileName : "index.html",
			syntaxCount : 2,
			semanticCount : 3,
			deprecatedCount : 3,
			practiceCount : 7,
			
			syntaxErrors : [
				{
					line : 1,
					column : 1,
					end: 3,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				},
				{
					line : 11,
					column : 4,
					end: 7,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				}
			],
			
			semanticErrors : [
				{
					line : 2,
					column : 1,
					end: 3,
					message : "semantic error",
					type: "semantic"
				},
				{
					line : 11,
					column : 1,
					end: 3,
					message : "hello there",
					type: "semantic"
				},
				{
					line : 9,
					column : 1,
					end: 3,
					message : "error there",
					type: "semantic"
				}
			],
			
			deprecatedErrors : [
				{
					line : 4,
					column : 1,
					end: 3,
					message : "dep error",
					type: "deprecated"
				},
				{
					line : 6,
					column : 1,
					end: 3,
					message : "what's dis",
					type: "deprecated"
				},
				{
					line : 4,
					column : 1,
					end: 3,
					message : "another error",
					type: "deprecated"
				}
			],
			
			practiceErrors : [
				{
					line : 4,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 6,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 4,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 2,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 11,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 9,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 4,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				}
			],
			
			sourceCode : [
				"<!doctype HTML>",
				"<html>",
				"<head>",
				"</head>",
				"<body>",
				"<a href=''>boopywoopy dsfffffffffffffffffffffffffsdkjfkdsjdskbfksjbfdkbdfskbdsfkbsdfkbdsfkbsdfkbsfdkdsbfkfsdbkfdsb",
				"</body>",
				"</div>",
				"</div>",
				"</disdv>",
				"</sdfdfs>",
				"</dsdfiv>",
				"</weew>",
				"</dfs>",
				"</sdfsdf>",
				"</didsfsdv>",
				"</disfdsdv>",
			]
			
		},
		{
			fileName : "about.html",
			syntaxCount : 4,
			semanticCount : 0,
			deprecatedCount : 0,
			practiceCount : 0,
			
			
			syntaxErrors : [
				{
					line : 1,
					column : 1,
					end: 3,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				},
				{
					line : 2,
					column : 1,
					end: 3,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				},
				{
					line : 6,
					column : 4,
					end: 12,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				},
				{
					line : 9,
					column : 1,
					end: 3,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				}
			],
			
			semanticErrors : [
			],
			
			deprecatedErrors : [
			],
			
			practiceErrors : [
			],
			
			sourceCode : [
				"<!doctype HTML>",
				"<second file woopy de woop>",
				"	<head>",
				"	</head>",
				"	<body>",
				"		<a href=''>boopywoopy dsfffffffffffffffffffffffffsdkjfkdsjdskbfksjbfdkbdfskbdsfkbsdfkbdsfkbsdfkbsfdkdsbfkfsdbkfdsb",
				"	</body>",
				"	</div>",
				"	</div>",
				"	</disdv>",
				"	</sdfdfs>",
				"	</dsdfiv>",
				"	</weew>",
				"	</dfs>",
				"	</sdfsdf>",
				"	</didsfsdv>",
				"	</disfdsdv>",
			]
			
		},
		{
			fileName : "contact.html",
			syntaxCount : 1,
			semanticCount : 2,
			deprecatedCount : 2,
			practiceCount : 2,
			
			
			syntaxErrors : [
				{
					line : 1,
					column : 1,
					end: 3,
					message : "language is an attribute that does not exist for this tag. Make sure you've spelt it correctly or that you're not using the attribute which belongs to another tag!",
					type: "syntax"
				}
			],
			
			semanticErrors : [
				{
					line : 2,
					column : 1,
					end: 3,
					message : "semantic error",
					type: "semantic"
				},
				{
					line : 11,
					column : 1,
					end: 3,
					message : "hello there",
					type: "semantic"
				}
			],
			
			deprecatedErrors : [
				{
					line : 4,
					column : 1,
					end: 3,
					message : "dep error",
					type: "deprecated"
				},
				{
					line : 6,
					column : 1,
					end: 3,
					message : "what's dis",
					type: "deprecated"
				}
			],
			
			practiceErrors : [
				{
					line : 4,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				},
				{
					line : 6,
					column : 1,
					end: 3,
					message : "For best practices, use the value attribute for every <input> tag.",
					type: "practice"
				}
			],
			
			sourceCode : [
				"<!THIRD FILE WOOP WOOP WOOP>",
				"<html>",
				"<head>",
				"</head>",
				"<body>",
				"<a href=''>boopywoopy dsfffffffffffffffffffffffffsdkjfkdsjdskbfksjbfdkbdfskbdsfkbsdfkbdsfkbsdfkbsfdkdsbfkfsdbkfdsb",
				"</body>",
				"</div>",
				"</div>",
				"</disdv>",
				"</sdfdfs>",
				"</dsdfiv>",
				"</weew>",
				"</dfs>",
				"</sdfsdf>",
				"</didsfsdv>",
				"</disfdsdv>",
			]
			
		}
	
	];
	
	// console.log("Going to set results with", $scope.oldFiles);
	
	// resultsService.setResults($scope.oldFiles);
	
	// console.log("What are the current results?", resultsService.getResults());
	
	// $scope.prepMultipleFiles = function() {
	
		// var numberOfFiles = $scope.multipleFiles.length;
		
		// for(var i = 0; i < numberOfFiles; i++) {
			// $scope.multipleFiles[i].fileNumber = i;
		// }
	
	// }
	
	// $scope.prepMultipleFiles();
	
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
	
	if($scope.multipleFiles.length > 1) {
	
		$scope.areMultipleFiles = true;
	
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
		console.log("@#@Data to be used for results:", $scope.multipleFiles);
		//$scope.multipleFiles = $scope.oldFiles; // !!! REMOVE THIS !!!
	}
	
	$scope.prepCounts = function() {
		var syntaxTotalCount = 0;
		var semanticTotalCount = 0;
		var deprecatedTotalCount = 0;
		var practiceTotalCount = 0;
		
		for(var i = 0; i < $scope.multipleFiles.length ; i++) {
			syntaxTotalCount += $scope.multipleFiles[0].syntaxErrors.length;
			$scope.multipleFiles[0].syntaxCount = syntaxTotalCount;
			semanticTotalCount += $scope.multipleFiles[0].semanticErrors.length;
			$scope.multipleFiles[0].semanticCount = semanticTotalCount;
			deprecatedTotalCount += $scope.multipleFiles[0].deprecatedErrors.length;
			$scope.multipleFiles[0].deprecatedCount = deprecatedTotalCount;
			practiceTotalCount += $scope.multipleFiles[0].practiceErrors.length;
			$scope.multipleFiles[0].practiceCount = practiceTotalCount;
			
		}
		
		$scope.totalSyntax = syntaxTotalCount;
		$scope.totalSemantic = semanticTotalCount;
		$scope.totalDeprecated = deprecatedTotalCount;
		$scope.totalPractice = practiceTotalCount;
		
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
				console.log("What is the error type?: " + errorType);
				console.log("i = " + i + ", j = " + j + " k = " + k);
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






