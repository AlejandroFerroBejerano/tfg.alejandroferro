/* -*- mode: js; coding: utf-8 -*- */

oshoziApp.controller("EventLogCtrl", function($scope, $http, $location, $timeout) {


  $scope.sortType = 'type'; // set the default sort type
  $scope.sortReverse = true;  // set the default sort order
  $scope.searchMessage = '';     // set the default search/filter term

  $scope.state = [
    {class_name: "danger", status: '0', tname: 'Alarma'},
    {class_name: "success", status: '1', tname: 'Reposo'},
    {class_name: "info", status: '2', tname: 'Omitido'},
    {class_name: "warning", status: '3', tname: 'Tamper'},
    {class_name: "warning", status: '4', tname: 'Cortocircuito'},
  ];

/*  $scope.message = [
    {idmsg:'1', date:'13/07/2016' ,time:'21:00' ,type:'CM' ,description:'CM PTA. OFICINAS', location: 'Planta Baja', status:'0', group:'Magnéticos'},
    {idmsg:'2', date:'13/07/2016' ,time:'21:00' ,type:'IR' ,description:'IR PTA. OFICINAS', location: 'Planta Baja', status:'0', group:'Volumétricos'},
    {idmsg:'3', date:'13/07/2016' ,time:'21:01' ,type:'CM' ,description:'CM PTA. ENT PPAL IZQ', location:'Planta Baja', status:'1', group:'Magnéticos'},
    {idmsg:'4', date:'13/07/2016' ,time:'21:01' ,type:'CM' ,description:'CM PTA. ENT PPAL DER', location:'Planta Baja', status:'2', group: 'Magnéticos'}
  ];*/
    
  $scope.get_color = function(status) {
    return $scope.state[status].class_name;
  };

  $scope.get_name = function(status) {
    return $scope.state[status].tname;
  };

  $scope.refresh = function() {
    $http.get('data/events.json').success(function(events) {
      $scope.events = events;
    }).error(function(){
      $scope.error = "Could not load Events information";
    });
  };

  $scope.clean_cloak = function(){
    $timeout(function(){
    angular.element('#div1').removeClass("my-cloak");
    angular.element(document.querySelector('#div1')).removeClass("my-cloak");
    });
  };

  $scope.url = $location.host();
  $scope.url_port = $location.port();

  $scope.error = null;

  $http.get('data/events.json')
	.success(function(events) {
	    $scope.events = events;
	})
	.error(function() {
	    $scope.error = "Could not load Events information";
	});
});
