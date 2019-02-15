'use strict';

angular
  .module('app')
  .service('authService', ["$q", "lock", "$http", "authManager",
           function ($q, lock, $http, authManager) {
    var userProfile = JSON.parse(localStorage.getItem('profile')) || null;
    var deferredProfile = $q.defer();

    if (userProfile) {
      deferredProfile.resolve(userProfile);
    };

    function getProfileDeferred() {
      return deferredProfile.promise;
    };

    function login() {
      lock.show();
    };

    function signup() {
      lock.show({allowLogin: false}); 
    };

    // Logging out just requires removing the user's
    // id_token and profile
    function logout() {
      localStorage.removeItem('id_token');
      localStorage.removeItem('profile');
      authManager.unauthenticate();

    };

    // Set up the logic for when a user authenticates
    // This method is called from app.run.js
    function registerAuthenticationListener() {
      lock.on('authenticated', function (authResult) {
        localStorage.setItem('id_token', authResult.idToken);
        authManager.authenticate();
        lock.getProfile(authResult.idToken, function (error, profile) {
          if (error) { return console.log(error); }
          localStorage.setItem('profile', JSON.stringify(profile));
          deferredProfile.resolve(profile);
        });
      });
    };
    return {
      login: login,
      logout: logout,
      signup: signup,
      registerAuthenticationListener: registerAuthenticationListener,
      getProfileDeferred: getProfileDeferred
    };
  }])




  .service('projectService', ["$q", "$http", "authService",
           function ($q, $http, authService) {
    
    var static_project;
    var static_project_list;

    function getProject() {
      var deferred = $q.defer();
      $http.get('/get_project')
        .success(function (data, status) {
          if (data.result) {
            static_project_list = angular.copy(data.project_list);
            deferred.resolve(data.project_list);
          }
        });
      return deferred.promise;
    };

    function postProject(project) {
      $http.post('/post_project', {'project': project});
    };

    function testerF(something) {
      console.log(something);
      $http.post("/show_project/" + something);
    };

    return {
      testerF: testerF,
      getProject: getProject,
      postProject: postProject,
    }
  }])




  .service('userService', ["$q", "$http", "authService",
           function ($q, $http, authService) {
    
    var static_profile;
    var static_skill = [];
    var static_role = [];
    var static_work = '';
    var static_project;

    function getProfile() {
      var deferred = $q.defer();
      var user_template = { email: '',
                            user_type: '',
                            given_name: '',
                            family_name: '',
                            phone: '',
                            address: '',
                            city: '',
                            state: '',
                            zipcode: '',
                            linkedin: '',
                            website: '',
                            result: false};
      $http.get('/get_profile')
        .success(function (data, status) {
          
          if (data.result) {
            static_profile = angular.copy(data.user);
            deferred.resolve(data.user);
          }
          else {
            authService.getProfileDeferred()
              .then(function (profile) {
                user_template['email'] = profile['email'];
                if (profile['identities'][0]['isSocial']) {
                  user_template['given_name'] = profile['given_name'];
                  user_template['family_name'] = profile['family_name'];
                }
                else {
                  user_template['given_name'] = profile['user_metadata']['given_name'];
                  user_template['family_name'] = profile['user_metadata']['family_name'];
                }
              });
            deferred.resolve(user_template);
          }
        });
      return deferred.promise;
    };

    function saveProfile(user) {
      if (!angular.equals(user, static_profile)) {
        $http.post('/save_profile', {'user': user});
        static_profile = angular.copy(user);
        console.log("Profile is not the same. Need to be update.");
      }
      else {
        console.log("Profile is the same.");
      }
    };

    function getSkill() {
      var deferred = $q.defer();
      var temp_skill;
      $http.get('/get_skill')
        .success(function (data, status) {
          if (data.result) {
            static_skill = data.skill.split(',');
            static_skill.pop();
            temp_skill = angular.copy(static_skill);
            deferred.resolve(temp_skill);
          }
          else {
            deferred.resolve([]);
          }
          
        });
      return deferred.promise;
    };

    function saveSkill(skill_tags) {
      var skill_str = '';
      if (!angular.equals(skill_tags, static_skill)) {
        for (var i=0; i<skill_tags.length; i++) {
          skill_str = skill_str + skill_tags[i] + ','
        };
        $http.post('/save_skill', {'skill': skill_str});
        static_skill = angular.copy(skill_tags);
        console.log("Skill is not the same. Need to be update.");
      }
      else {
        console.log("Skill is the same.");
      }
    };

    function getRole() {
      var deferred = $q.defer();
      var temp_role;
      $http.get('/get_role')
        .success(function (data, status) {
          if (data.result) {
            static_role = data.role.split(',');
            static_role.pop();
            temp_role = angular.copy(static_role);
            deferred.resolve(temp_role);
          }
          else {
            deferred.resolve([]);
          }
          
        });
      return deferred.promise;
    };

    function saveRole(role_tags) {
      var role_str = '';
      if (!angular.equals(role_tags, static_role)) {
        for (var i=0; i<role_tags.length; i++) {
          role_str = role_str + role_tags[i] + ','
        };
        $http.post('/save_role', {'role': role_str});
        static_role = angular.copy(role_tags);
        console.log("Role is not the same. Need to be update.");
      }
      else {
        console.log("Role is the same.");
      }
    };

    function getWork() {
      var deferred = $q.defer();
      var temp_work = [];
      $http.get('/get_work')
        .success(function (data, status) {
          if (data.result) {
            static_work = data.work.split(' ');
            static_work.pop();
            for (var i=0; i<static_work.length; i++) {
              temp_work.push({'url': static_work[i]});
            };
            static_work = data.work;
            deferred.resolve(temp_work);
          }
          else {
            deferred.resolve([{'url':''}, {'url':''}, {'url':''}]);
          }
        });
      return deferred.promise;
    };

    function saveWork(works) {
      var work_str = '';
      for (var i=0; i<works.length; i++) {
          if (works[i]['url'] != '') {
            work_str = work_str + works[i]['url'] + ' ';
          };
      };
      console.log(work_str);
      console.log(works);
      console.log(static_work);
      if (!angular.equals(work_str, static_work)) {
        $http.post('/save_work', {'work': work_str});
        static_work = angular.copy(works);
        console.log("Work is not the same. Need to be update.");
      }
      else {
        console.log("Work is the same.");
      }
    };

    function temp1() {

    };

    function temp2() {

    };

    function temp3() {

    };

    return {
      getProfile: getProfile,
      getSkill: getSkill,
      getRole: getRole,
      getWork: getWork,
      saveProfile: saveProfile,
      saveSkill: saveSkill,
      saveWork: saveWork,
      saveRole: saveRole,
    };
  }])
