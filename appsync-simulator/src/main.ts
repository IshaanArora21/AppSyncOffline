import {
    AmplifyAppSyncSimulator,
    AmplifyAppSyncSimulatorAuthenticationType,
    AmplifyAppSyncSimulatorConfig,
} from 'amplify-appsync-simulator'

import { handler as graphQLHandler } from './resolvers/graphQLHandler'
import { schema } from "./schema"
import { readVTL } from './vtl/readVTL'
import { resolversConfig } from './resolversConfig'


class AppSyncSimulator {
    httpPort: number
    wssPort: number

    constructor(httpPort: number, wssPort: number) {
        this.httpPort = httpPort
        this.wssPort = wssPort
    }

    async start() {
        const simulatorConfig: AmplifyAppSyncSimulatorConfig = {
            appSync: {
                // Uncomment this for GraphQL sandbox
                defaultAuthenticationType: {
                    authenticationType: AmplifyAppSyncSimulatorAuthenticationType.AMAZON_COGNITO_USER_POOLS,
                    cognitoUserPoolConfig: {},
                },
                // Uncomment this for local development
                // defaultAuthenticationType: {
                //     authenticationType: AmplifyAppSyncSimulatorAuthenticationType.API_KEY
                // },
                name: 'api-local',
                additionalAuthenticationProviders: [],
                apiKey: 'dummy-api-key'
            },
            schema: { content: schema },
            mappingTemplates: [
                {
                    path: 'lambdaRequestMappingTemplate.vtl',
                    content: readVTL("lambdaRequestMappingTemplate.vtl"),
                },
                {
                    path: 'lambdaResponseMappingTemplate.vtl',
                    content: readVTL("lambdaResponseMappingTemplate.vtl"),
                }
            ],
            dataSources: [
                {
                    type: 'AWS_LAMBDA',
                    name: 'LambdaDataSource',
                    invoke: graphQLHandler,
                }
            ],
            resolvers: resolversConfig,
        }
        const amplifySimulator = new AmplifyAppSyncSimulator({
            port: this.httpPort,
            wsPort: this.wssPort,
        })
        await amplifySimulator.start()
        await amplifySimulator.init(simulatorConfig)
    }
}

const httpPort = 5000
const wsPort = 5001
const simulator = new AppSyncSimulator(httpPort, wsPort)
simulator.start().then(() => {
    console.log(`🚀 App Sync Simulator started at http://localhost:${httpPort}/graphql`)
})