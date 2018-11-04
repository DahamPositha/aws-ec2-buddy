/**
 * Created by Daham Pathiraja on 5/29/18.
 */

import commandLineArgs from 'command-line-args';
import PythonShell from 'python-shell';
import {spotModel} from './model/spot/spotModel';
import * as constants from './helpers/constants';

//node dist/index.js -m spot-history -t m4.2xlarge -s 1517346477 -e 1527356577

//node dist/index.js -m spot-price-comparison -t m4.2xlarge m4.4xlarge -s 1517346477 -e 1527356577

const optionDefinitions = [
    {name: 'method', alias: 'm', type: String},
    {name: 'instanceType', alias: 't', type: String, multiple: true, defaultOption: true},
    {name: 'start', alias: 's', type: Number},
    {name: 'end', alias: 'e', type: Number}
];

const options = commandLineArgs(optionDefinitions);

/**
 * plot
 */
function plot() {
    let options = {
        pythonPath: '/Library/Frameworks/Python.framework/Versions/2.7/bin/python',
        scriptPath: `${process.cwd()}/src/predictionModels`
    };
    PythonShell.run(`generate_predictions.py`, options, function (err) {
        if (err) throw err;
        console.log('finished');
    });
};

switch (options.method) {
    case 'spot-history':
        spotModel.getSpotHistoryAndStore(options.instanceType[0], options.startTime, options.endTime, constants.SPOT_HISTORY_OUT_FILE_1)
            .then(()=> {
                console.log('Success');
                plot();
            })
            .catch(()=> {
                console.log('Fail');
            })
        break;
    case 'spot-price-comparison':
        let instanceType1Price = new Promise(function (resolve, reject) {
            spotModel.getSpotHistoryAndStore(options.instanceType[0], options.startTime, options.endTime, constants.SPOT_HISTORY_OUT_FILE_1)
                .then(resolve)
                .catch(reject);
        });

        let instanceType2Price = new Promise(function (resolve, reject) {
            spotModel.getSpotHistoryAndStore(options.instanceType[1], options.startTime, options.endTime, constants.SPOT_HISTORY_OUT_FILE_2)
                .then(resolve)
                .catch(reject);
        });

        Promise.all([instanceType1Price, instanceType2Price]).then(function () {
            console.log("success");
        });
        break;
    default:
        break;

}
console.log(options.method);

