'use strict';

angular
  .module('app', ['auth0.lock', 'angular-jwt', 'ui.router', 'ngMaterial', 'ngMessages', 'angular-md5', 'material.svgAssetsCache'])
  .config(["$stateProvider", "lockProvider", "$urlRouterProvider", 'jwtOptionsProvider', '$httpProvider', '$mdThemingProvider',
    function ($stateProvider, lockProvider, $urlRouterProvider, jwtOptionsProvider, $httpProvider, $mdThemingProvider) {
    $urlRouterProvider.otherwise('/home');
    $stateProvider
      .state('home', {
        url: '/home',
        controller: 'homeCtrl as vm',
        templateUrl: 'static/home.html'})
      .state('news', {
        url: '/news',
        templateUrl: 'static/news.html'})
      .state('cases', {
        url: '/cases',
        templateUrl: 'static/cases.html'})
      .state('intro', {
        url: '/intro',
        templateUrl: 'static/introduction.html'})
      .state('signup', {
        url: '/signup',
        controller: 'signupCtrl as vm',
        loginAfterSignUp: true,
        templateUrl: 'static/signup.html'});

    $mdThemingProvider.theme('docs-dark', 'default')
          .primaryPalette('teal');


    lockProvider.init({
      clientID: 'dHCeAvImpUyvxssQpYZCG86OyZSJlXhH',
      domain: 'jiepang.auth0.com',
      options: {
        rememberLastLogin: true,
        // allowSignUp: false,
        auth: {
          // redirect: false,
          params: {
            scope: "openid email"
          }
        },
        theme: {
          logo: 'static/img/logo.png',
          primaryColor: "teal"
        },
        additionalSignUpFields: [{
            name: "given_name",
            placeholder: "Please enter your firt name",
            validator: function(given_name) {
                  return {
                     valid: given_name.length >= 0,
                     hint: "Must have" // optional
                  };
                }
          },
          {
            name: "family_name",
            placeholder: "Please enter your last name",
            validator: function(family_name) {
                  return {
                     valid: family_name.length >= 0,
                     hint: "Must have" // optional
                  };
                }
          }],
          languageDictionary: {
            title: "Welcome"
          }
      }
    });


  // Configuration for angular-jwt
      jwtOptionsProvider.config({
        tokenGetter: function () {
          return localStorage.getItem('id_token');
        },
        whiteListedDomains: ['localhost'],
        unauthenticatedRedirectPath: '/'
      });

      // Add the jwtInterceptor to the array of HTTP interceptors
      // so that JWTs are attached as Authorization headers
      $httpProvider.interceptors.push('jwtInterceptor');
  }])
  .run(['$rootScope', 'authService', 'lock', 'authManager', 'userService',
       function ($rootScope, authService, lock, authManager, userService) {
    // Put the authService on $rootScope so its methods
    // can be accessed from the nav bar
    $rootScope.authService = authService;
    $rootScope.userService = userService;

    // Register the authentication listener that is
    // set up in auth.service.js
    authService.registerAuthenticationListener();

    // Register the synchronous hash parser
    // when using UI Router
    lock.interceptHash();

    // Use the authManager from angular-jwt to check for
    // the user's authentication state when the page is
    // refreshed and maintain authentication
    authManager.checkAuthOnRefresh();
  }]);