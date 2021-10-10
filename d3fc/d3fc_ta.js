// import { indicatorExponentialMovingAverage } from '@d3fc/d3fc-technical-indicator';
import { indicatorMovingAverage } from './d3fc-technical-indicator.js';
import { indicatorExponentialMovingAverage } from './d3fc-technical-indicator.js';

// const movingAverage = indicatorMovingAverage()
//     .period(3);
app.indicatorMovingAverage = indicatorMovingAverage;
app.indicatorExponentialMovingAverage = indicatorExponentialMovingAverage;
// console.log(exponentialMovingAverage([5, 6, 7, 6, 5, 4]));