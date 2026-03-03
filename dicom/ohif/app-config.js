dataSources: [
  {
    namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
    sourceName: 'dicomweb',
    configuration: {
      friendlyName: 'Orthanc',

      qidoRoot: 'http://localhost:8042/dicom-web',
      wadoRoot: 'http://localhost:8042/dicom-web',
      wadoUriRoot: 'http://localhost:8042/wado',

      requestOptions: {
        requestHeaders: {
          Authorization: 'Basic b3J0aGFuYzpvcnRoYW5j',
        },
      },

      supportsIncludeField: true,
      imageRendering: 'wadors',
      thumbnailRendering: 'wadors',
      enableStudyLazyLoad: true,
    },
  },
],
