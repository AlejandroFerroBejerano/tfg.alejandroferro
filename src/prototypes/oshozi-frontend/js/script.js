(function() {
// script.js
// create the module and name it panelApp
// also include ngRoute for all our routing needs
	var oshoziApp = angular.module('oshoziApp', ['ngRoute']);

	// configure our routes
	oshoziApp.config(function($routeProvider) {
		$routeProvider

		    // route for the home page
		    .when('/', {
		        templateUrl : 'pages/home.html',
		        controller  : 'mainController'
		    })

		    // route for the about page
		    .when('/event_monitor', {
		        templateUrl : 'pages/event_monitor.html',
		        controller  : 'event_monitorController'
		    })

		    // route for the contact page
		    .when('/configuration', {
		        templateUrl : 'pages/configuration.html',
		        controller  : 'configController'
		    });
	});


	// create the controller and inject Angular's $scope
	oshoziApp.controller('mainController', function($scope) {
		// create a message to display in our view
	});

	oshoziApp.controller('event_monitorController', function($scope) {

		$scope.sortType = 'type'; // set the default sort type
  	$scope.sortReverse = true;  // set the default sort order
  	$scope.searchMessage = '';     // set the default search/filter term

		$scope.message = [
			{idmsg:'1', date:'13/07/2016' ,time:'21:00' ,type:'CM' ,description:'CM PTA. OFICINAS', location: 'Planta Baja', status:'Alarma', group:'Magnéticos'},
			{idmsg:'2', date:'13/07/2016' ,time:'21:00' ,type:'IR' ,description:'IR PTA. OFICINAS', location: 'Planta Baja', status:'Alarma', group:'Volumétricos'},
			{idmsg:'3', date:'13/07/2016' ,time:'21:01' ,type:'CM' ,description:'CM PTA. ENT PPAL IZQ', location:'Planta Baja', status:'Alarma', group:'Magnéticos'},
			{idmsg:'4', date:'13/07/2016' ,time:'21:01' ,type:'CM' ,description:'CM PTA. ENT PPAL DER', location:'Planta Baja', status:'Alarma', group: 'Magnéticos'}
		];
	});

	oshoziApp.controller('configController', function() {
		this.description='';
		this.addButton = function(button){
			button.description = this.description;
			console.log("this -> "+ button.description);
			
		};
		
	});

	oshoziApp.controller('TabController', function(){
    	this.tab = 1;

    	this.setTab = function(tab){
      		this.tab = tab;
    	};

    	this.isSet = function(tab){
      	return (this.tab === tab);
    	};
	});


		var buttons = [
      {idButton:'13', state:false ,mode:'output' ,type:'digital' ,description:'Comedor'},
      {idButton:'12', state:false ,mode:'output' ,type:'digital' ,description:'Salon'},
      {idButton:'11', state:false ,mode:'output' ,type:'digital' ,description:'Dormitorio principal'},
      {idButton:'10', state:false ,mode:'output' ,type:'digital' ,description:'Dormitorio 2'},
      {idButton:'9', state:false ,mode:'output' ,type:'digital' ,description:'Dormitorio 3'},
      {idButton:'8', state:false ,mode:'output' ,type:'digital' ,description:'Entrada'},
      {idButton:'7', state:false ,mode:'output' ,type:'digital' ,description:'Aseo 1'},
      {idButton:'6', state:false ,mode:'output' ,type:'digital' ,description:'Cocina'},
      {idButton:'5', state:false ,mode:'output' ,type:'digital' ,description:'Aseo 2'}
    ];

})();
