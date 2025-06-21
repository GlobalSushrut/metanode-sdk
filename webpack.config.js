const path = require('path');

module.exports = {
  entry: './index.js',
  output: {
    filename: 'metanode.min.js',
    path: path.resolve(__dirname, 'dist'),
    library: 'MetaNode',
    libraryTarget: 'umd',
    globalObject: 'this'
  },
  target: 'node',
  node: {
    __dirname: false
  },
  externals: {
    'child_process': 'commonjs child_process',
    'fs': 'commonjs fs',
    'path': 'commonjs path'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  }
};
