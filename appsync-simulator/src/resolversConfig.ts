import { AppSyncSimulatorPipelineResolverConfig, AppSyncSimulatorUnitResolverConfig, RESOLVER_KIND } from "amplify-appsync-simulator";

export const resolversConfig: (AppSyncSimulatorPipelineResolverConfig | AppSyncSimulatorUnitResolverConfig)[] = [
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "Query",
    //     fieldName: "users",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "Query",
    //     fieldName: "user",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "Query",
    //     fieldName: "getUserById",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "User",
    //     fieldName: "job",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "User",
    //     fieldName: "friends",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    // {
    //     kind: RESOLVER_KIND.UNIT,
    //     typeName: "Mutation",
    //     fieldName: "createUser",
    //     dataSourceName: "LambdaDataSource",
    //     requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
    //     responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    // },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Query",
        fieldName: "getAllUsers",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Query",
        fieldName: "getAllWalkInDrives",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    }
]