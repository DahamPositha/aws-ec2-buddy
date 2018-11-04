/**
 * Created by Daham Pathiraja on 5/29/18.
 */

import AWS from 'aws-sdk';
import FileUtils from "../utils/fileUtils";
import * as constants from '../helpers/constants';

/**
 * This class initializes AWS EC2 client and exposes various services of it.
 */
export default class AwsEc2Client {
    /**
     * Init services and variables
     */
    constructor() {
        let awsConfig = FileUtils.loadConfigs(constants.AWS_CONFIG);
        AWS.config.update({
            region: awsConfig[constants.REGION]
        });

        this.ec2 = new AWS.EC2({
            accessKeyId: awsConfig[constants.ACCESS_KEY_ID],
            secretAccessKey: awsConfig[constants.SECRET_ACCESS_KEY]
        });
    }

    /**
     * Describes the Spot price history
     */
    describeSpotPriceHistory({AvailabilityZone, EndTime, InstanceTypes, ProductDescriptions, StartTime}) {
        let _this = this;

        return new Promise((resolve, reject)=> {
            _this.ec2.describeSpotPriceHistory({
                AvailabilityZone,
                EndTime,
                InstanceTypes,
                ProductDescriptions,
                StartTime
            }, function (err, data) {
                if (err) {
                    console.log(err, err.stack);
                    return reject();
                }
                return resolve(data);
            });
        });

    }

}

export const awsEc2Client = new AwsEc2Client();
