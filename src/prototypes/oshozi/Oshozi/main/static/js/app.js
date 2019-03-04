/* -*- mode: js; coding: utf-8 -*- */

oshoziApp = angular.module(
    "oshoziApp", [],

    function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
    }
);
