window.config = {
  routerBasename: '/',
  showStudyList: true,

  dataSources: [
    {
      sourceName: 'dicomweb',
      configuration: {
        friendlyName: 'Orthanc',
        name: 'orthanc',

        qidoRoot: 'http://localhost:8042/dicom-web',
        wadoRoot: 'http://localhost:8042/dicom-web',
        wadoUriRoot: 'http://localhost:8042/wado',

        supportsIncludeField: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,
      },
    },
  ],
};
