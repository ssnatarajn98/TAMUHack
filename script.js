(function(angular) {
  'use strict';
// declare a module
var myAppModule = angular.module('myApp', []);

myAppModule.controller('MainController', ['$scope', '$http', function($scope, $http) {
$http({
    method: 'GET',
    url: "item-types.json"

}).then((types_array) => {
    $http({
        method: 'GET',
        url: "item-list.json"
    }).then((items_array) => {
        let types = types_array.data.data.reduce( (acc,type) =>  {
            acc[type["ItemTypeId"]] = type["TypeName"];
            return acc;
        }, {});
        $scope.items = items_array.data.data.reduce( (acc,item) => {
            let type = types[item["ItemTypeId"]];
            if (! (type in acc) )
                acc[type] = [];
            acc[type].push(item);

            return acc;
        }, {});

    })
});
                  
}]);

})(window.angular);
