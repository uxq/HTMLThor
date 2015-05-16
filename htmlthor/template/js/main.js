var htmlthorApp = angular.module('htmlthorApp', ['ngRoute', 'ui.router', 'ngSanitize', 'ngFileUpload']);

htmlthorApp.config(function($stateProvider, $locationProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider
        .state('home',
            {
				controller: 'UploadController',
                url: '/',
                templateUrl: '/static/partials/_home.html',
				activeTab: 'home'
            }
        )
		.state('resources',
            {
                url: '/resources',
                templateUrl: '/static/partials/_resources.html',
				activeTab: 'resources'
            }
        )
		.state('about',
            {
                url: '/about',
                templateUrl: '/static/partials/_about.html',
				activeTab: 'about'
            }
        )
		.state('results',
            {
				controller: 'ResultsController',
                url: '/results',
                templateUrl: '/static/partials/_results.html',
				activeTab: 'results'
            }
        )
		.state('temp',
            {
				controller: 'ResultsController',
                url: '/temp',
                templateUrl: '/static/partials/_temp.html',
				activeTab: 'results'
            }
        )

});

htmlthorApp.filter('trustHtml', function ($sce) {
    return function (val) {
        return $sce.trustAsHtml(val);
    };
});

htmlthorApp.controller('MainController', function($scope, $state) {
	//console.log("Loaded main controller!");
	$scope.state = $state;
});

htmlthorApp.service('resultsService', function() {

	var currentResults = [];
	
	var setResults = function(newResults) {
		//console.log("Setting current results", newResults);
		currentResults = newResults;
	}
	
	var getResults = function() {
		//console.log("Getting results", currentResults);
		return currentResults;
	}
	
	return {
		setResults : setResults,
		getResults : getResults
	};
	
});

//   $routeProvider
//       .when('/', {
//           templateUrl:'templates/_home.html',
//           controller: 'HomeCtrl'
//       }).when('/work/:type', {
//           templateUrl:'templates/_work.html',
//           controller: 'WorkCtrl'
//       })
//       .otherwise({redirectTo: '/'});
