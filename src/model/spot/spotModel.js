/**
 * Created by Daham Pathiraja on 5/29/18.
 */

import {awsEc2Client} from "../../consumers/awsEc2Client";
import CsvWriter from "../../utils/csvWriter";

/**
 * This Model is for getting Spot instance related data.
 */
export default class SpotModel {
    /**
     *
     * @param instanceType
     * @param startTime
     * @param endTime
     * @param outFile
     * @returns {Promise}
     */
    getSpotHistoryAndStore(instanceType, startTime, endTime, outFile) {
        return new Promise((resolve, reject)=> {
            awsEc2Client.describeSpotPriceHistory({
                AvailabilityZone: 'us-east-1a',
                EndTime: endTime,
                InstanceTypes: [
                    instanceType
                ],
                ProductDescriptions: [
                    "Linux/UNIX (Amazon VPC)"
                ],
                StartTime: startTime
            }).then((data)=> {
                let spotPriceHistory = [];
                data.SpotPriceHistory.forEach(function (e) {
                    spotPriceHistory.push({
                        'Timestamp': e.Timestamp,
                        SpotPrice: e.SpotPrice
                    });
                });
                return spotPriceHistory;
            }).then((spotPriceHistory)=> {
                console.log(spotPriceHistory);
                return new CsvWriter(outFile).writeJsonAsCsv(spotPriceHistory);
            }).then(resolve)
                .catch(()=> {
                    console.log("Error occurred while processing");
                });
        });
    }
}

export const spotModel = new SpotModel();