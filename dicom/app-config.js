window.config = {
  routerBasename: '/',
  showStudyList: true,
  extensions: [],
  modes: [],
  dataSources: [
    {
      namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
      sourceName: 'orthanc',
      configuration: {
        friendlyName: 'Orthanc',
        name: 'orthanc',
        qidoRoot: 'http://127.0.0.1:8042/dicom-web',
        wadoRoot: 'http://127.0.0.1:8042/dicom-web',
        wadoUriRoot: 'http://127.0.0.1:8042/wado',
        staticWado: true,
        singlepart: 'bulkdata',
        enableStudyLazyLoad: true,
        supportsFuzzyMatching: false,
        supportsWildcard: true
      }
    }
  ],
  defaultDataSourceName: 'orthanc'
};
