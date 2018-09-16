// main.cpp file for Tutorial 5 - Mastering Monero

#include "cryptonote_core/tx_pool.h"
#include "cryptonote_core/blockchain.h"

#include "blockchain_db/lmdb/db_lmdb.h"

#include "easylogging++.h"

#include "common/base58.h"

#include "crypto/crypto-ops.h"
#include "crypto/keccak.h"

// Converts crypto::hash into crypto::secret_key or crypto::public_key

template <typename T>
T get_key_from_hash(crypto::hash & in_hash){
	T* key;
	key = reinterpret_cast<T*>(&in_hash);
	return *key;
}

int main(){
  	// Put here your private spendable key!
	std::string str_spend_key = "20ae8eae3d02072e627d3f74141507aec6fe899154193d6d3ce5da6621b3060a";
	cryptonote::network_type nettype = cryptonote::MAINNET;	
	crypto::public_key public_spend_key;

	// convert hex string to binary data
	cryptonote::blobdata blob;
	epee::string_tools::parse_hexstr_to_binbuff(str_spend_key, blob);
	crypto::secret_key sc = reinterpret_cast<crypto::secret_key &>(blob);

	// generate public key based on the private key
	crypto::secret_key_to_public_key(sc, public_spend_key);
	
	std::cout << "Public spend key : "  << public_spend_key  << std::endl;
	
	crypto::hash hash_of_private_spend_key;
	
	keccak((uint8_t *)&str_spend_key, sizeof(str_spend_key), (uint8_t *)&str_spend_key, sizeof(str_spend_key));

	crypto::secret_key private_view_key;
	crypto::public_key public_view_key;
	
	crypto::generate_keys(public_view_key,private_view_key,get_key_from_hash<crypto::secret_key>(hash_of_private_spend_key), true);
	
	std::cout << "\n" << "Private view key : "  << private_view_key << std::endl;
	std::cout << "Public view key  : "  << public_view_key  << std::endl;
  

	cryptonote::account_public_address address {public_spend_key, public_view_key};
	std::string address_n ;

	address_n = cryptonote::get_account_address_as_str(nettype, false, address); 
	std::cout << "Monero Address:" << address_n << std::endl;

	return 0;
}
