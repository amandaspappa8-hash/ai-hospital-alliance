import { BrowserProvider, Contract } from "ethers";
const CONTRACT_ADDRESS = import.meta.env.VITE_MEDICAL_REPORT_NFT_ADDRESS;
const MEDICAL_REPORT_NFT_ABI = [
    "function tokenCounter() view returns (uint256)",
    "function reports(uint256) view returns (string reportId, string reportHash, string metadataURI)",
    "function mintReport(address patient, string reportId, string reportHash, string metadataURI) returns (uint256)"
];
export async function getBlockchainReady() {
    if (!window.ethereum) {
        throw new Error("MetaMask not found");
    }
    const provider = new BrowserProvider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    const signer = await provider.getSigner();
    const address = await signer.getAddress();
    const contract = new Contract(CONTRACT_ADDRESS, MEDICAL_REPORT_NFT_ABI, signer);
    return {
        provider,
        signer,
        address,
        contract
    };
}
export async function mintMedicalReportNFT(params) {
    const { contract } = await getBlockchainReady();
    const tx = await contract.mintReport(params.patient, params.reportId, params.reportHash, params.metadataURI);
    const receipt = await tx.wait();
    const total = await contract.tokenCounter();
    return {
        txHash: receipt?.hash ?? "",
        totalTokens: Number(total)
    };
}
export async function readMedicalReport(tokenId) {
    const { contract } = await getBlockchainReady();
    const report = await contract.reports(tokenId);
    return {
        reportId: report.reportId,
        reportHash: report.reportHash,
        metadataURI: report.metadataURI
    };
}
