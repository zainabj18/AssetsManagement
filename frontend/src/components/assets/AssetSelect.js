import React,{useEffect, useMemo,useState} from 'react';
import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Modal,
	ModalOverlay,
	ModalContent,
	ModalHeader,
	ModalFooter,
	ModalBody,
	ModalCloseButton,
	useDisclosure,
	Button,
	HStack,
	Box,
	Checkbox,
	Input,
	VStack,
} from '@chakra-ui/react';
import AssetTable from './AssetTable';



function AssetSelect({setSelected,assetsin}) {
	const { isOpen, onClose,onOpen, } = useDisclosure();
	const [selected,setAssetSelected] = useState([]); 

	const save=()=>{
		console.log('Selected',selected);
		setSelected(selected);
		onClose();
	};

	useEffect(() => {
	  console.log('here');
	}, [assetsin]);
	

	return (<>
		<Button onClick={onOpen}>Select Assets</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent bgGradient= "linear(to-l, #4E65FF, #92EFFD)">
				<ModalHeader>Asset Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{assetsin && <AssetTable assets={assetsin} setSelectedAssets={setAssetSelected} preSelIDs={selected}/>}
				</ModalBody>
				<ModalFooter>
					<HStack>
						<Button onClick={save}>Save</Button>
					</HStack>	
				</ModalFooter>
			</ModalContent>
			
		</Modal>
	</>
	);
}

export default AssetSelect;