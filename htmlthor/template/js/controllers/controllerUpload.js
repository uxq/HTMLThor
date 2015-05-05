//thorpedoFile

//thorpedoUrl

//thorpedoDirect

htmlthorApp.controller('UploadController', function ($location, $http, $scope, Upload, resultsService) {

	$scope.userUrl = "http://www.";
	$scope.userDirect = "";
	$scope.validUrl = "false";

	console.log("Upload Controller loaded.");
	
	$scope.isValidUrl = function() {
		console.log("Checking if valid url using", $scope.userUrl);
		//^(http|https|ftp)?(:\/\/)?(www|ftp)?.?[a-z0-9-]+(.|:)([a-z0-9-]+)+([\/?].*)?$
		// var regexp = /^(http|https|ftp)?(:\/\/)?(www|ftp)?.?[a-z0-9-]+(.|:)([a-z0-9-]+)+([\/?].*)?$/;
		// var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
		var regexp = /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;
		console.log("Testing result: ", regexp.test($scope.userUrl));
		return regexp.test($scope.userUrl);   
	}
	
	$scope.isValidDirect = function() {
		return $scope.userDirect.length > 1;
	}

	$scope.initUploadButton = function() {
		var uploadButton = $("#button--uploadFiles");
		var uploadInput = $("#input--uploadFiles");
		
		//console.log("Initialized the upload stuff...", uploadButton, uploadInput);
		
		uploadButton.click(function() {
			uploadInput.click();
			//console.log("Clicked button and clicked input");
		});
		
		uploadInput.change(function() {
			var selectedFiles = uploadInput[0].files;
			//console.log("Selected some files", uploadInput.val(), selectedFiles);
			//$scope.uploadFiles(selectedFiles);
			$scope.upload(selectedFiles);
		});
		
	}

	$scope.upload = function (files) {
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                Upload.upload({
                    url: '/thorpedoFile/',
                    fields: {},
                    file: file
                }).progress(function (evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                }).success(function (data, status, headers, config) {
                    console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
                });
            }
        }
    };

	$scope.uploadFiles = function(selectedFiles) {

		if(selectedFiles.length == 0) return;

		//var fd = new FormData();
        //fd.append('file', selectedFiles[0]);

		// $http.post('/thorpedoFile/', {
		// 	file: selectedFiles[0]
		// }, {
  //           // transformRequest: angular.identity,
  //           headers: {'Content-Type': 'multipart/form-data'}
  //       })
  //       .success(function(d){
  //       })
  //       .error(function(d){
  //       });

		$http({
            method: 'POST',
            url: "/thorpedoFile/",
            headers: { 'Content-Type': undefined },
            data: {
            	file: selectedFiles[0]
            }
        }).
        success(function (data, status, headers, config) {
            //alert("success!");
        }).
        error(function (data, status, headers, config) {
            //alert("failed!");
        });

		// if(selectedFiles.length == 1) {
		// 	var singleFile = selectedFiles[0];
		// 	var singleFileName = singleFile.name;
		// 	var singleFileExtension = singleFileName.substr(singleFileName.lastIndexOf('.') + 1);
		// 	if (singleFileExtension == "html" || singleFileExtension == "php" || singleFileExtension == "zip") {
		// 		console.log("Individual file!!!", singleFileName, singleFileExtension);
		// 		$scope.submitIndividualUpload(singleFile);
		// 	} else {
		// 		console.log("Incorrect file type", singleFileName, singleFileExtension);
		// 	}
		// } else {
		// 	console.log("Multiple files!!!");
		// 	for(var i = 0; i < selectedFiles.length; i++) {
		// 		var thisFileExtension = selectedFiles[i].name.substr(singleFileName.lastIndexOf('.') + 1);
		// 		if (thisFileExtension == "html" || thisFileExtension == "php" || thisFileExtension == "zip") {
		// 			console.log("Individual file!!!", thisFileExtension);
		// 		} else {
		// 			console.log("Incorrect file type", thisFileExtension);
		// 		}
		// 	}
		// }
	}

	$scope.initDirectInput = function() {
		var directInput = $("#input--home-direct");
		var submitButton = $("#button--directInput");
		
		submitButton.click(function() {
			if(directInput.val().length == 0) {
				console.log("Nothing entered...");
				return;
			}
			$scope.submitDirectInput(directInput.val());
		});
		
	}

	$scope.submitIndividualUpload = function(file) {

		console.log("File size is: " + file.size);
		if(file.size > 10000) {
			console.log("File size maybe a bit too big?");
		}
		
		var reader = new FileReader();
		reader.readAsText(file, 'UTF-8');
		reader.onload = $scope.continuedUpload;

	}

	$scope.continuedUpload = function(event) {
		
		var urlToUse = "/thorpedoFile/";
		var dataToSend = event.target.result;
		
		console.log("I'm going to submit the following: ", dataToSend);
		
		
		$.ajax({
		  type: "POST",
		  url: urlToUse,
		  contentType: "application/json",
		  // dataType: "json",
			// contentType:"multipart/form-data; boundary=frontier",
			contentType: false,
		  data: dataToSend,
		  success: function(data){
			console.log("!!!!!!!!Submitted successfully!", data);
		  },
		  error: function(data) {
			console.log("@@@Failed to send / do stuff", data);
		  }
		  // dataType: dataType
		});
		

	}

	$scope.submitDirectInput = function(directCode) {
		
		var urlToUse = "/thorpedoDirect/";
		// var dataToSend = {};
		// dataToSend.input = directCode;
		var dataToSend = directCode;
		
		// var csrftoken = $.cookie('csrftoken');
		
		console.log("I'm going to submit the following: ", dataToSend);
		$scope.setSiteLoading();
		//boop
		
		$.ajax({
		  type: "POST",
		  url: urlToUse,
		  contentType: false,
		  // dataType: "json",
			//contentType:"multipart/form-data",
		  data: dataToSend,
		  success: function(data){
			console.log("!!!!!!!!Submitted successfully!", data);
			$("body").addClass("state--receivedResults");
			$scope.removeSiteLoading();
			resultsService.setResults(data);
			$scope.redirectToResults();
			// time to change to the results page
		  },
		  error: function(data) {
			console.log("@@@Failed to send / do stuff", data);
			$scope.removeSiteLoading();
		  }
		  // dataType: dataType
		});
			
		// $http({
		// url: urlToUse,
			// method: "POST",
			// data: dataToSend
		// }).success(function(data, status, headers, config) {
			
			// console.log("!!!!!!!!Submitted successfully!", data);
			
		// }).error(function(data, status, headers, config) {
		
			// console.log("ERROR, DIDN'T SUBMIT PROPERLY", status);
			
		// });
		
	}
	
	$scope.setSiteLoading = function() {
		$("body").addClass("state--validating");
	}
	
	$scope.removeSiteLoading = function() {
		$("body").removeClass("state--validating");
	}
	
	$scope.redirectToResults = function() {
		console.log("Redirecting to results page...");
		$location.path('/results');
		$scope.$apply();
	}
	
	$scope.initUploadButton();
	$scope.initDirectInput();

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
