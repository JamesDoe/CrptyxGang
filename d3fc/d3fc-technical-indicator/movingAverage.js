// https://stackoverflow.com/questions/47844765/d3-rebind-in-d3-v4/47845718
function rebind(target, source) {
    var i = 1,
      n = arguments.length,
      method;
    while (++i < n) target[method = arguments[i]] = d3_rebind(target, source, source[method]);
    return target;
  };
  
  function d3_rebind(target, source, method) {
    return function() {
      var value = method.apply(source, arguments);
      return value === source ? target : value;
    };
  }

import _slidingWindow from './slidingWindow';

export default function() {

    const slidingWindow = _slidingWindow()
        .accumulator(values => values && d3.mean(values));

    const movingAverage = data => slidingWindow(data);

    rebind(movingAverage, slidingWindow, 'period', 'value');

    return movingAverage;
}