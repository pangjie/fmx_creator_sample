'use strict';

angular
  .module('app')
  .controller("navCtrl", ["$q", "$scope", "authService",
              function ($q, $scope, authService) {
  }])
  .controller("signupCtrl", ["$q", "$scope", "$http", "authService", "$mdConstant", "userService",
              function ($q, $scope, $http, authService, $mdConstant, userService) {
  }])

  .controller("homeCtrl", ["authService", "$mdConstant", "userService", "projectService", "md5", "$rootScope",
              function (authService, $mdConstant, userService, projectService, md5, $rootScope) {
    
    var vm = this;
    vm.project = {};
    
    if ($rootScope.isAuthenticated) {
      userService.getProfile().then(function (data) {vm.user = data;});
      userService.getSkill().then(function (data) {vm.skill = data;});
      userService.getRole().then(function (data) {vm.selected = data;});
      userService.getWork().then(function (data) {vm.works = data;});
      authService.getProfileDeferred().then(function (data) {vm.profile = data;});

      projectService.getProject().then(function (data) {vm.project_list = data;});
    }
    
    // Dashboard

    vm.ttest = function () {
      projectService.testerF(2);
    };


    // Workshop
    
    vm.post_project = function () {
      vm.project.pid = md5.createHash(vm.project.name.replace(/\s+/g, '').toLowerCase())
      vm.project.status = 'new';
      projectService.postProject(vm.project);
    };


    // Profile
    vm.save = function () {
      userService.saveProfile(vm.user);
      userService.saveSkill(vm.skill);
      userService.saveRole(vm.selected);
      userService.saveWork(vm.works);
    };

    vm.add_work = function () {
      vm.works.push({'url':''});
    };
    
    vm.remove_work = function (index) {
      vm.works.splice(index, 1);
    };

    vm.toggle = function (item, list) {
      var idx = list.indexOf(item);
      if (idx > -1) {
        list.splice(idx, 1);
      }
      else {
        list.push(item);
      }
    };

    vm.exists = function (item, list) {
      return list.indexOf(item) > -1;
    }; 

    vm.states = ('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS ' +
    'MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI ' +
    'WY').split(' ').map(function(state) { return {abbrev: state}; });

    vm.keys = [$mdConstant.KEY_CODE.ENTER, 
               $mdConstant.KEY_CODE.COMMA,
               $mdConstant.KEY_CODE.SEMICOLON];

    vm.usertype = 2;

    vm.items = ['VR Cinema Photographer', 
                'VR Director', 
                'VR Script Writer', 
                'Post Production Editor',
                'Stitching', 
                'Special Effect',
                'Games Programmer', 
                '2D Animation Designers', 
                '3D Animation Designers', 
                '3D Sound Engineers'];
    vm.selected = [];

    // User Classification
    vm.user_classification = function (user_classification) {
      vm.selectedIndex = 2;
      vm.user['user_type'] = user_classification;
      userService.saveProfile(vm.user);
    };
    // vm.selectedIndex = 1
  }]);


