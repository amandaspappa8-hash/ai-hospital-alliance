window.config = {
  routerBasename: '/',
  showStudyList: true,

  servers: {
    dicomWeb: [
      {
        name: 'orthanc',
        wadoUriRoot: 'http://localhost:8042/dicom-web',
        qidoRoot: 'http://localhost:8042/dicom-web',
        wadoRoot: 'http://localhost:8042/dicom-web',
        qidoSupportsIncludeField: true,
        imageRendering: 'wadouri',
        thumbnailRendering: 'wadouri',
        enableStudyLazyLoad: true,
        supportsFuzzyMatching: false,
      },
    ],
  },
};
