import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import FilterBasedSearch from './routes/FilterBasedSearch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/AssetsOverview';



function App() {
	
	return (
		<AuthProvider>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route path="/" element={<Layout />}>
					<Route index path="assets" element={<AssetsOverview />} />
					<Route path="newasset" element={<CreateAsset />} />
					<Route path="asset/:id" element={<AssetViewer canEdit={true} isNew={false}/>} />
					<Route path="filter" element={<FilterBasedSearch />} />
					<Route path="user" element={<User />} />
					<Route path="type/adder" element={<TypeAdder />} />
				</Route>
				<Route path="*" element={<NoMatch />} />
			</Routes>
		</AuthProvider>
	);
}

export default App;
