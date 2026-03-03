window.config = {
  routerBasename: '/',
  showStudyList: true,

  dataSources: [
    {
      sourceName: 'dicomweb',
      configuration: {
        friendlyName: 'Orthanc',
        name: 'orthanc',

        // داخل Docker: خليها orthanc وليس localhost
        qidoRoot: 'http://orthanc:8042/dicom-web',
        wadoRoot: 'http://orthanc:8042/dicom-web',

        supportsIncludeField: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,

        // ✅ هنا مكان الدالة/البلوك
        requestOptions: {
          requestHeaders: {
            Authorization: 'Basic b3J0aGFuYzp vcnRoYW5j'.replace(' ', ''),
          },
        },
      },
    },
  ],
};
