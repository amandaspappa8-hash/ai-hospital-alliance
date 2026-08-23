window.config = {
  routerBasename: '/',
  showStudyList: true,
  dataSources: [
    {
      namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
      sourceName: 'Orthanc',
      configuration: {
        friendlyName: 'Orthanc',
        name: 'Orthanc',
        qidoRoot: 'http://127.0.0.1:8042/dicom-web',
        wadoRoot: 'http://127.0.0.1:8042/dicom-web',
        wadoUriRoot: 'http://127.0.0.1:8042/wado',
        qidoSupportsIncludeField: true,
        supportsWildcard: true,
        supportsFuzzyMatching: false,
        supportsReject: false,
        supportsBulkDataURI: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,
      },
    },
  ],
  defaultDataSourceName: 'Orthanc',
}
