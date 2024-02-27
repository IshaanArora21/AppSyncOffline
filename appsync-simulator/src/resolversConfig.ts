import { AppSyncSimulatorPipelineResolverConfig, AppSyncSimulatorUnitResolverConfig, RESOLVER_KIND } from "amplify-appsync-simulator";

export const resolversConfig: (AppSyncSimulatorPipelineResolverConfig | AppSyncSimulatorUnitResolverConfig)[] = [
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Query",
        fieldName: "getAllWalkInDrives",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
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
        fieldName: "getWalkInDriveByGUID",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Query",
        fieldName: "getUserByGUID",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Mutation",
        fieldName: "login",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Mutation",
        fieldName: "applyDrive",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
    {
        kind: RESOLVER_KIND.UNIT,
        typeName: "Mutation",
        fieldName: "createUser",
        dataSourceName: "LambdaDataSource",
        requestMappingTemplateLocation: "lambdaRequestMappingTemplate.vtl",
        responseMappingTemplateLocation: "lambdaResponseMappingTemplate.vtl"
    },
]