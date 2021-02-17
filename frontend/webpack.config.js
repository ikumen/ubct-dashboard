const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');

const mode = process.env.NODE_ENV || 'development';
const prod = mode === 'production';

module.exports = {
	entry: {
		bundle: ['./app/main.js']
	},
	resolve: {
		alias: {
			svelte: path.resolve('node_modules', 'svelte')
		},
		extensions: ['.mjs', '.js', '.svelte'],
		mainFields: ['svelte', 'browser', 'module', 'main']
	},
	output: {
		path: __dirname + '/public/static',
		filename: '[name].js',
		publicPath: '/static/',
		chunkFilename: '[name].[id].js'
	},
	devServer: {
		liveReload: false,
		disableHostCheck: true,
		watchContentBase: true,
		contentBase: __dirname + '/public',
		headers: {
			'Access-Control-Allow-Origin': '*'
		}, 
		historyApiFallback: {
      rewrites: [
        { from: /^\/$/, to: '/index.html' },
      ],
    },
		proxy: {
			'/api': 'http://localhost:5000',
			'/signin': 'http://localhost:5000',
			'/signout': 'http://localhost:5000',
			'/dataset': 'http://localhost:5000',
		}
	},
	module: {
		rules: [
			{
				test: /\.svelte$/,
				use: {
					loader: 'svelte-loader',
					options: {
						emitCss: true,
						hotReload: false
					}
				}
			},
			{
				test: /\.css$/,
				use: [
					/**
					 * MiniCssExtractPlugin doesn't support HMR.
					 * For developing, use 'style-loader' instead.
					 * */
					prod ? MiniCssExtractPlugin.loader : 'style-loader',
					'css-loader'
				]
			}
		]
	},
	mode,
	plugins: [
		new MiniCssExtractPlugin({
			filename: '[name].css',
			linkType: 'text/css'
		})
	],
	devtool: prod ? false: 'source-map',
	watchOptions: {
		ignored: /node_modules/,
		poll: 2000
  }
};
