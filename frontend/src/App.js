import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/assets/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import AssetSearcher from './routes/AssetSearcher';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import TypeViewer from './routes/TypeViewer';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import SubLayout from './routes/assets/SubLayout';
import AssetList from './components/AssetList';
import CreateProject from './routes/CreateProject';
import { Box, Button } from '@chakra-ui/react';
import AdminManager from './routes/AdminManager';
import RelatedAssetViewer from './components/RelatedAssetViewer';
import Tags from './routes/Tags';
import TagViewer from './routes/TagViewer';
import AssetOverview from './components/AssetOverview';
import AssetLogs from './routes/assets/AssetLogs';
import RelatedTags from './routes/assets/RelatedTags';
import RelatedProjects from './routes/assets/RelatedProjects';
import RelatedClassification from './routes/assets/RelatedClassification';
//TODO:Wrap in error boundary
function App() {

	return (
		<AuthProvider>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route path="/" element={<Layout />}>
					<Route path="assets/" element={<SubLayout name="Assets"/>}>
						<Route index element={<AssetsOverview />} />
						<Route path="new" element={<CreateAsset />} />
						<Route path="view/:id" element={<AssetOverview />}>
							<Route index element={<AssetViewer canEdit={true} isNew={false}/>} />	
							<Route path="logs" element={<AssetLogs />} />	
							<Route path="tags" element={<RelatedTags />} />	
							<Route path="projects" element={<RelatedProjects />} />	
							<Route path="classification" element={<RelatedClassification />} />	
						</Route>
						<Route path="related" element={<RelatedAssetViewer canEdit={true} isNew={false}/>} />
					</Route>

					<Route path="tags/" element={<Tags />}>
						<Route path=":id" element={<TagViewer/>} />	
					</Route>
					<Route path="projects/" element={<SubLayout name="Projects"/>}>
						<Route index element={<NavLink to="./new">Create New Project</NavLink>} />
						<Route path="new" element={<CreateProject />} />
					</Route>
					<Route path="type/" element={<SubLayout name="Types"/>}>
						<Route index element={<TypeViewer />} />
						<Route path="adder" element={<TypeAdder />} />
					</Route>
					<Route path="accounts" element={<AdminManager />} />
					<Route path="user" element={<User />} />
				</Route>
				<Route path="*" element={<NoMatch />} />
			</Routes>
		</AuthProvider>

	);
}

export default App;
