var app = angular.module('app', ['rzModule']);

app.factory('ServerRequest', function ($http) {
  return {
    'get_values': function () {
      return $http.get('/values');
    },
    'set_brightness': function (brightness) {
      return $http.get('/brightness?value=' + brightness);
    },
    'set_pixels': function (pixels) {
      return $http.post('/pixels', pixels);
    }
  };
});

app.factory('Server', function ($q, $rootScope, ServerRequest) {
  var error_handler = function (res) {
    if (res.status === 0) {
       $rootScope.errorStatus = 'No connection. Verify application is running.';
    } else if (res.status == 400) {
       $rootScope.errorStatus = 'Invalid Server Request [400]';
    } else if (res.status == 500) {
       $rootScope.errorStatus = 'Internal Server Error [500].';
    }

    return $q.reject(res);
  };

  return {
    'get_values': function () {
      return ServerRequest.get_values()
        .then(function (res) {
          return res.data;
        }, error_handler);
    },
    'set_brightness': function (brightness) {
      return ServerRequest.set_brightness(brightness)
        .then(function () {
          return brightness;
        }, error_handler);
    },
    'set_pixels': function (pixels) {
      return ServerRequest.set_pixels(pixels)
        .then(function () {
          return pixels;
        }, error_handler);
    }
  }
});

app.controller('LightController', function($scope, Server) {
  $scope.brightness = {
    value: 0,
    options: {
      step: 10,
      floor: 0,
      ceil: 100,
      interval: 1000,
      hideLimitLabels: true,
      translate: function (value) {
        return '';
      }
    }
  };
  $scope.pixels = null;
  $scope.ready = false;

  $scope.colors = [
    "#660000","#990000","#cc0000","#cc3333",
    "#ea4c88","#993399","#663399","#333399",
    "#0066cc","#0099cc","#66cccc","#77cc33",
    "#669900","#336600","#666600","#999900",
    "#cccc33","#ffff00","#ffcc33","#ff9900",
    "#ff6600","#cc6633","#996633","#663300",
    "#ffffff"
  ];

  $scope.$watch('brightness.value', function (value) {
    if(!$scope.ready) {
      return;
    }
    Server.set_brightness(value/100);
  });

  Server.get_values()
    .then(function (data) {
      $scope.brightness.value = data.brightness*100;
      $scope.pixels = data.pixels;
      $scope.ready = true;
    });

  $scope.getPixelWidthCount = function () {
    $scope.pixels.length / 2;
  };

  $scope.getPixelWidth = function() {
    return new Array($scope.getPixelWidthCount());
  };

  $scope.getBackgroundColor = function (pixel) {
    return 'rgb(' + pixel[0]*255 + ',' + pixel[1]*255 + ',' + pixel[2]*255 + ')';
  };

  $scope.changeColor = function (index, color) {
    var pixels = angular.copy($scope.pixels);
    pixels[index] = $scope.hexToRgb(color);
    Server.set_pixels(pixels)
      .then(function (pixels) {
        $scope.pixels = pixels;
      });
  };

  $scope.hexToRgb = function(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16) / 255,
        parseInt(result[2], 16) / 255,
        parseInt(result[3], 16) / 255
    ] : null;
  };

  $scope.compareColor = function (pixel, color) {
    var rgb = $scope.hexToRgb(color);
    return pixel[0] == rgb[0] && pixel[1] == rgb[1] && pixel[2] == rgb[2];
  };
});