import { Routes, Route} from 'react-router-dom';
import AssetViewer from './components/assets/AssetVeiwer';
import AssetOverview from './components/assets/AssetOverview';
import Layout from './components/layouts/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import TypeViewer from './routes/TypeViewer';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import SubLayout from './components/layouts/SubLayout';
import CreateProject from './routes/CreateProject';
import AdminManager from './routes/AdminManager';
import Tags from './routes/Tags';
import TagViewer from './routes/TagViewer';
import AssetLogs from './routes/assets/AssetLogs';
import RelatedToTable from './components/assets/RelatedToTable';
import AttributeViewer from './routes/AttributeViewer';
import ProjectViewer from './routes/ProjectViewer';
import TypeEditor from './routes/TypeEditor';
import Logs from './routes/Logs';
import Comments from './routes/assets/Comments';
import { fetchRelatedClassification, fetchRelatedFrom, fetchRelatedProjects, fetchRelatedTags, fetchRelatedTo, fetchRelatedType } from './api';
function App() {

	return (
		<AuthProvider>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route path="/" element={<Layout />}>
					<Route path="assets/" element={<SubLayout name="Assets"/>}>
						<Route index element={<AssetsOverview />} />
						<Route path="new" element={<AssetViewer />} />
						<Route path=":id" element={<AssetOverview />}>
							<Route index element={<AssetViewer />} />	
							<Route path="comments" element={<Comments />} />	
							<Route path="logs" element={<AssetLogs />} />
							<Route path="type" element={<RelatedToTable relatedFunc={fetchRelatedType}/>} />	
							<Route path="classification" element={<RelatedToTable relatedFunc={fetchRelatedClassification}/>} />
							<Route path="tags" element={<RelatedToTable relatedFunc={fetchRelatedTags}/>} />
							<Route path="projects" element={<RelatedToTable relatedFunc={fetchRelatedProjects}/>} />
							<Route path="outgoing" element={<RelatedToTable relatedFunc={fetchRelatedFrom}/>} />
							<Route path="incomming" element={<RelatedToTable relatedFunc={fetchRelatedTo}/>} />
						</Route>
					</Route>
					<Route path="projects/" element={<SubLayout name="Projects"/>}>
						<Route index element={<ProjectViewer/>} />
						<Route path="new" element={<CreateProject />} />
					</Route>

					<Route path="tags/" element={<Tags />}>
						<Route path=":id" element={<TagViewer/>} />	
					</Route>
					<Route path="type/" element={<SubLayout name="Types"/>}>
						<Route index element={<TypeViewer />} />
						<Route path="adder" element={<TypeAdder />} />
						<Route path="attributes" element={<AttributeViewer />} />
						<Route path=":id" element={<TypeEditor />} />
					</Route>
					<Route path="accounts" element={<AdminManager />} />
					<Route path="user" element={<User />} />
					<Route path="logs" element={<Logs />} />
				</Route>
				<Route path="*" element={<NoMatch />} />
			</Routes>
		</AuthProvider>

	);
}

export default App;
