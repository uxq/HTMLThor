//thorpedoFile

//thorpedoUrl

//thorpedoDirect

htmlthorApp.controller('UploadController', function ($location, $http, $scope, $sce, Upload, resultsService) {

	$scope.userUrl = "http://www.";
	$scope.userDirect = "";
	$scope.validUrl = "false";
	$scope.errorSubmitting = false;

	//console.log("Upload Controller loaded.");
	
	$scope.isValidUrl = function() {
		//console.log("Checking if valid url using", $scope.userUrl);
		//^(http|https|ftp)?(:\/\/)?(www|ftp)?.?[a-z0-9-]+(.|:)([a-z0-9-]+)+([\/?].*)?$
		// var regexp = /^(http|https|ftp)?(:\/\/)?(www|ftp)?.?[a-z0-9-]+(.|:)([a-z0-9-]+)+([\/?].*)?$/;
		// var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
		var regexp = /^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;
		//console.log("Testing result: ", regexp.test($scope.userUrl));
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

	// This is the one being used!
	$scope.upload = function (files) {
        if (files && files.length) {
        	$scope.setSiteLoading();

        	var arrayOfFiles = [];
        	var namesOfFiles = [];

            for (var i = 0; i < files.length; i++) { // probably redundant atm
                var file = files[i];
                arrayOfFiles.push(file);
                namesOfFiles.push(file.name);
            }

            console.log("About to push to api with this data", arrayOfFiles, namesOfFiles);

            //var extension = file.name.split(".");
            //extension = extension[extension.length-1];
            Upload.upload({
                url: '/thorpedoFile/',
                //fields: {file_extension: extension},
                file: arrayOfFiles,
                fileFormDataName: namesOfFiles,
            }).progress(function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                //console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            }).success(function (data, status, headers, config) {
                //console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
        		resultsService.setResults(data);
        		$scope.redirectToResults();
        		$scope.removeSiteLoading();
            }).error(function() {
            	console.log("ERROR, SOMETHING WENT WRONG!");
            	$("#input--uploadFiles").wrap('<form>').closest('form').get(0).reset();
 				$("#input--uploadFiles").unwrap();
            	$scope.errorSubmitting = true;
            	$scope.removeSiteLoading();
            });


            // for (var i = 0; i < files.length; i++) {
            //     var file = files[i];
            //     $scope.setSiteLoading();
            //     var extension = file.name.split(".");
            //     extension = extension[extension.length-1];
            //     Upload.upload({
            //         url: '/thorpedoFile/',
            //         fields: {file_extension: extension},
            //         file: file
            //     }).progress(function (evt) {
            //         var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            //         //console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            //     }).success(function (data, status, headers, config) {
            //         //console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            // 		resultsService.setResults(data);
            // 		$scope.redirectToResults();
            // 		$scope.removeSiteLoading();
            //     });
            // }

        }
    };

	$scope.initDirectInput = function() {
		var directInput = $("#input--home-direct");
		var submitButton = $("#button--directInput");
		
		submitButton.click(function() {
			if(directInput.val().length == 0) {
				//console.log("Nothing entered...");
				return;
			}
			$scope.submitDirectInput(directInput.val());
		});
		
	}

	$scope.submitDirectInput = function(directCode) {
		
		var urlToUse = "/thorpedoDirect/";
		// var dataToSend = {};
		// dataToSend.input = directCode;
		var dataToSend = $sce.trustAsHtml(directCode);

		var dataToSend = urlencode(dataToSend);
		
		// var csrftoken = $.cookie('csrftoken');
		
		console.log("I'm going to submit the following: ", dataToSend);
		$scope.setSiteLoading();

		//boop

		$http({
		    method: 'POST',
		    url: '/thorpedoDirect/',
		    data: "body="+dataToSend,
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data){
			resultsService.setResults(data);
            $scope.redirectToResults();
            $scope.removeSiteLoading();
		}).error(function() {
			$scope.errorSubmitting = true;
        	$scope.removeSiteLoading();
		});
		
	}
	
	$scope.setSiteLoading = function() {
		$("body").addClass("state--validating");
	}
	
	$scope.removeSiteLoading = function() {
		$("body").removeClass("state--validating");
	}
	
	$scope.redirectToResults = function() {
		//console.log("Redirecting to results page...");
		$location.path('/results');
		//$scope.$apply();
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

function urlencode(str) {
  //       discuss at: http://phpjs.org/functions/urlencode/
  //      original by: Philip Peterson
  //      improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  //      improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  //      improved by: Brett Zamir (http://brett-zamir.me)
  //      improved by: Lars Fischer
  //         input by: AJ
  //         input by: travc
  //         input by: Brett Zamir (http://brett-zamir.me)
  //         input by: Ratheous
  //      bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  //      bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  //      bugfixed by: Joris
  // reimplemented by: Brett Zamir (http://brett-zamir.me)
  // reimplemented by: Brett Zamir (http://brett-zamir.me)
  //             note: This reflects PHP 5.3/6.0+ behavior
  //             note: Please be aware that this function expects to encode into UTF-8 encoded strings, as found on
  //             note: pages served as UTF-8
  //        example 1: urlencode('Kevin van Zonneveld!');
  //        returns 1: 'Kevin+van+Zonneveld%21'
  //        example 2: urlencode('http://kevin.vanzonneveld.net/');
  //        returns 2: 'http%3A%2F%2Fkevin.vanzonneveld.net%2F'
  //        example 3: urlencode('http://www.google.nl/search?q=php.js&ie=utf-8&oe=utf-8&aq=t&rls=com.ubuntu:en-US:unofficial&client=firefox-a');
  //        returns 3: 'http%3A%2F%2Fwww.google.nl%2Fsearch%3Fq%3Dphp.js%26ie%3Dutf-8%26oe%3Dutf-8%26aq%3Dt%26rls%3Dcom.ubuntu%3Aen-US%3Aunofficial%26client%3Dfirefox-a'

  str = (str + '')
    .toString();

  // Tilde should be allowed unescaped in future versions of PHP (as reflected below), but if you want to reflect current
  // PHP behavior, you would need to add ".replace(/~/g, '%7E');" to the following.
  return encodeURIComponent(str)
    .replace(/!/g, '%21')
    .replace(/'/g, '%27')
    .replace(/\(/g, '%28')
    .
  replace(/\)/g, '%29')
    .replace(/\*/g, '%2A')
    .replace(/%20/g, '+');
}